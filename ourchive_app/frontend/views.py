from django.shortcuts import render
import requests
from django.conf import settings
from django.views.decorators.http import require_http_methods

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

@require_http_methods(["GET"])
def works(request):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'works.html', {'work_types': work_types['results']})

def works_by_type(request, type_id):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	# todo: get works by type
	return render(request, 'works.html', {'work_types': work_types['results']})

def new_work(request):
	return render(request, 'works.html', {'work_types': work_types['results']})

def edit_work(request, id):
	return render(request, 'works.html', {'work_types': work_types['results']})

@require_http_methods(["GET"])
def work(request, pk):
	chapter_offset = int(request.GET.get('offset', 0))
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/'+str(pk))
	work = response.json()
	if chapter_offset == 0:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/'+str(pk)+'/chapters?limit=1')
	else:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/'+str(pk)+'/chapters?limit=1&offset='+str(chapter_offset))
	chapter = response.json()
	return render(request, 'work.html', {'work_types': work_types['results'], 
		'work': work,
		'chapter': chapter['results'][0],
		'next_chapter': settings.ALLOWED_HOSTS[0] + '/works/'+str(pk)+'?offset='+str(chapter_offset + 1) if chapter['next'] else None,
		'previous_chapter': settings.ALLOWED_HOSTS[0] + '/works/'+str(pk)+'?offset='+str(chapter_offset - 1)  if chapter['previous'] else None,})

def bookmarks(request):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'bookmarks.html', {'work_types': work_types['results']})

def bookmark(request, pk):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'bookmark.html', {'work_types': work_types['results']})
