from django.conf import settings

class FileHelperService:
	def get_service():
		if settings.FILE_PROCESSOR == 'local':
			return LocalFileHelper()
		else:
			return None

class LocalFileHelper:	
	def handle_uploaded_file(self, f, name):
		content_type = 'image/' if 'image' in f.content_type else 'audio/' if 'audio' in f.content_type else ''
		with open(settings.MEDIA_ROOT + '/' + content_type + name, 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)

	def handle_file_serve(self, prepend, filename):
		some_file = self.model.objects.get(imported_file=filename)
		response = FileResponse(some_file.imported_file)
		# https://docs.djangoproject.com/en/1.11/howto/outputting-csv/#streaming-large-csv-files
		response['Content-Disposition'] = 'attachment; filename="%s"'%filename
		return response