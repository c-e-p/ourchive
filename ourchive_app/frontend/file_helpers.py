from django.conf import settings
import logging
import boto3
from botocore.exceptions import ClientError
import uuid

class FileHelperService:
	def get_service():
		if settings.FILE_PROCESSOR == 'local':
			return LocalFileHelper()
		elif settings.FILE_PROCESSOR == 's3':
			return S3FileHelper()
		else:
			return None

class FileCommon:
	def get_filename(self, original_name):
		uuid = str(uuid.uuid4())
		return uuid + '_' + original_name

class LocalFileHelper:	
	common = FileCommon()

	def handle_uploaded_file(self, file, name, username):
		filename = common.get_filename(file)
		content_type = 'image/' if 'image' in file.content_type else 'audio/' if 'audio' in file.content_type else ''
		with open(settings.MEDIA_ROOT + '/' + content_type + username + "/" + filename, 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)

	def handle_file_serve(self, prepend, filename):
		some_file = self.model.objects.get(imported_file=filename)
		response = FileResponse(some_file.imported_file)
		# https://docs.djangoproject.com/en/1.11/howto/outputting-csv/#streaming-large-csv-files
		response['Content-Disposition'] = 'attachment; filename="%s"'%filename
		return response

class S3FileHelper:
	def handle_uploaded_file(self, file, name, username):
		"""Upload a file to an S3 bucket

		:param file: File to upload
		:param name: Filetype subdirectory
		:return: True if file was uploaded, else False
		"""
		# Upload the file
		s3_client = boto3.client('s3')
		try:
			response = s3_client.upload_fileobj(file, settings.S3_BUCKET, file.name)
		except ClientError as e:
			logging.error(e)
			return False
		return True