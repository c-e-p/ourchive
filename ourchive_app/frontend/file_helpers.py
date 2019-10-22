from background_task import background
from django.conf import settings

def handle_uploaded_file(f, name):
	with open(settings.MEDIA_ROOT + '/' + name, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)