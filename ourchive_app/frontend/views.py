from django.shortcuts import render, redirect
import requests
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.models import User

def index(request):
	return render(request, 'index.html', {
	    'heading_message': 'Welcome to Ourchive',
	    'long_message': 'Ourchive is a configurable, extensible, multimedia archive, meant to serve as a modern alternative to PHP-based archives. You can search for existing works, create your own, or create curated collections of works you\'ve enjoyed. Have fun with it!'
	})

def search(request):
	return render(request, 'search.html', {})

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
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	if request.user.is_authenticated:
		return render(request, 'work_form.html', {'work_types': work_types['results'],
			'work': {}})
	else:
		messages.add_message(request, messages.ERROR, 'You must log in to post a new work.')	
		return redirect('/login')

def group_tags(tag_types, tags):
	result = {}
	for tag_type in tag_types:
		result[tag_type['label']] = []
	for tag in tags:
		result[tag['tag_type']].append(tag)
	return result

def edit_work(request, id):
	if request.method == 'POST':
		messages.add_message(request, messages.ERROR, 'An error occurred while updating the work.')	
		return redirect('/works/'+id)
	else:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
		work_types = response.json()
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/tagtypes')
		tag_types = response.json()
		if request.user.is_authenticated:
			response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/'+str(id))
			work = response.json()
			if work['user_id'] != request.user.id:			
				messages.add_message(request, messages.ERROR, 'You are not authorized to edit this work.')	
				return redirect('/')
			tags = group_tags(tag_types['results'], work['tags'])
			return render(request, 'work_form.html', {'work_types': work_types['results'],
				'work': work, 
				'tags': tags})
		else:
			messages.add_message(request, messages.ERROR, 'You must log in to post a new work.')	
			return redirect('/login')

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
		return render(request, 'login.html', {})

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
		return render(request, 'register.html', {})

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
	return render(request, 'bookmarks.html', {})

def bookmark(request, pk):
	return render(request, 'bookmark.html', {})
