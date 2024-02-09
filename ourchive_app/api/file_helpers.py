from django.conf import settings
import logging
import boto3
from botocore.exceptions import ClientError
import uuid
import os
import pathlib
import audioread
from api.models import OurchiveSetting


logger = logging.getLogger(__name__)


class FileHelperService:
    def get_service():
        if settings.FILE_PROCESSOR == 'local':
            return LocalFileHelper()
        elif settings.FILE_PROCESSOR == 's3':
            return S3FileHelper()
        else:
            return None


class FileCommon:
    ALLOWED_TYPES = ['epub', 'pdf', 'mp4', 'mp3', 'm4b', 'mobi', 'm4a', 'zip']

    def get_filename(self, original_name):
        suffix = pathlib.Path(original_name).suffix
        trimmed_filename = original_name.split(suffix)[0]
        original_name = ''.join(e for e in trimmed_filename if e.isalnum())
        uuid_str = str(uuid.uuid4())
        return uuid_str + '_' + original_name + suffix

    def calculate_audio_duration(self, filename):
        audio_processing = (OurchiveSetting.objects.filter(name='Audio Processing').first() is not None and OurchiveSetting.objects.filter(name='Audio Processing').first().value == 'True')
        if audio_processing:
            try:
                with audioread.audio_open(filename) as f:
                    # TODO: move processing to celery/bg task
                    print(f.duration)
            except audioread.DecodeError:
                logging.error(f"File could not be decoded: {filename}")

    def get_allowed_content_types(self, content_type):
        for allowed_type in self.ALLOWED_TYPES:
            if allowed_type in content_type:
                return True
        return False


class LocalFileHelper:
    common = FileCommon()

    def handle_uploaded_file(self, file, name, username):
        filename = self.common.get_filename(name)
        content_type = 'image/' if 'image' in file.content_type else 'audio/' if 'audio' in file.content_type else 'upload/' if self.common.get_allowed_content_types(file.content_type) else None
        if not content_type:
            print(f"CONTENT TYPE: {file.content_type}")
            return None
        full_name = settings.MEDIA_ROOT + '/' + content_type + username + "/" + filename
        logging.debug(f"File upload: {full_name}")
        os.makedirs(os.path.dirname(full_name), exist_ok=True)
        with open(full_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        if (content_type == 'audio/'):
            self.common.calculate_audio_duration(full_name)
        return settings.MEDIA_URL + content_type + username + "/" + filename

    def handle_file_serve(self, prepend, filename):
        some_file = self.model.objects.get(imported_file=filename)
        response = FileResponse(some_file.imported_file)
        # https://docs.djangoproject.com/en/1.11/howto/outputting-csv/#streaming-large-csv-files
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response


class S3FileHelper:
    common = FileCommon()

    def handle_uploaded_file(self, file, name, username):
        """Upload a file to an S3 bucket

        :param file: File to upload
        :param name: Filetype subdirectory
        :return: True if file was uploaded, else False
        """
        # Upload the file
        s3_client = boto3.client('s3')
        filename = self.common.get_filename(file.name)
        try:
            response = s3_client.upload_fileobj(file, settings.S3_BUCKET, filename)
        except ClientError as e:
            logging.error(e)
            return filename
        return None
