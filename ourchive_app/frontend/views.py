from django.shortcuts import render, redirect
import requests
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.models import User

def index(request):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	print(request.user)
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
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	return render(request, 'work_form.html', {'work_types': work_types['results']})

def log_in(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		if user is not None:
			login(request, user)
			messages.add_message(request, messages.SUCCESS, 'Login successful.')		
			return redirect('/')
		else:
			messages.add_message(request, messages.ERROR, 'Login unsuccessful. Please try again.')
			return redirect('/login')
	else:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
		work_types = response.json()
		return render(request, 'login.html', {'work_types': work_types['results']})

def register(request):
	if request.method == 'POST':
		user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'))
		if user is not None:
			messages.add_message(request, messages.SUCCESS, 'Registration successful!')		
			return redirect('/')
		else:
			messages.add_message(request, messages.ERROR, 'Registration unsuccessful. Please try again.')
			return redirect('/login')
	else:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
		work_types = response.json()
		return render(request, 'register.html', {'work_types': work_types['results']})

def log_out(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'Logout successful.')		
	return redirect('/')


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
