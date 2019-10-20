from django.shortcuts import render
import requests
from django.conf import settings

def index(request):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'index.html', {
	    'work_types': work_types['results'],
	    'message': 'Hello! This is some scaffolding to determine effective view architecture. Stay tuned!'
	})
