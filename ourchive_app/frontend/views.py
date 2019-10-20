from django.shortcuts import render
import requests
from django.conf import settings

def index(request):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'index.html', {
	    'work_types': work_types['results'],
	    'heading_message': 'Welcome to Ourchive',
	    'long_message': 'Ourchive is a configurable, extensible, multimedia archive, meant to serve as a modern alternative to PHP-based archives. You can search for existing works, create your own, or create curated collections of works you\'ve enjoyed. Have fun with it!'
	})

def search(request):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'search.html', {'work_types': work_types['results']})

def works(request):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'works.html', {'work_types': work_types['results']})

def works_by_type(request, type_id):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	# todo: get works by type
	return render(request, 'works.html', {'work_types': work_types['results']})

def work(request, pk):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'work.html', {'work_types': work_types['results']})

def bookmarks(request):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'bookmarks.html', {'work_types': work_types['results']})

def bookmark(request, pk):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'bookmark.html', {'work_types': work_types['results']})
