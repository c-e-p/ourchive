from django.shortcuts import render, redirect
import requests
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.models import User
import json
from . import file_helpers
import threading
from django.http import HttpResponse

def index(request):
	return render(request, 'index.html', {
	    'heading_message': 'Welcome to Ourchive',
	    'long_message': 'Ourchive is a configurable, extensible, multimedia archive, meant to serve as a modern alternative to PHP-based archives. You can search for existing works, create your own, or create curated collections of works you\'ve enjoyed. Have fun with it!'
	})

def user_name(request, username):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/users/'+username)
	print(response)
	user = response.json()
	return render(request, 'user.html', {'user': user})

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
	if request.user.is_authenticated and request.method != 'POST':
		return render(request, 'work_form.html', {'work_types': work_types['results'],
			'work': {}})
	elif request.user.is_authenticated:
		return edit_work(request, -1)
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

def edit_chapter(request, id):
	if request.method == 'POST':
		if 'files[]' in request.FILES:
			file_helpers.handle_uploaded_file(request.FILES['files[]'], request.FILES['files[]'].name)
			return HttpResponse(request.FILES['files[]'].name)
		else:
			headers = {}
			headers['X-CSRFToken'] = request.COOKIES['csrftoken']
			headers['content-type'] = 'application/json'
			response = requests.put(settings.ALLOWED_HOSTS[0] + '/api/chapters/' + str(id) +'/', data=json.dumps(request.POST), cookies=request.COOKIES, headers=headers)
			if response.status_code == 200:
				messages.add_message(request, messages.SUCCESS, 'Chapter updated.')	
			elif response.status_code == 403:
				messages.add_message(request, messages.ERROR, 'You are not authorized to update this chapter.')	
			else:
				print(response.status_code)
				print(response.content)
				messages.add_message(request, messages.ERROR, 'An error has occurred while updating this chapter. Please contact your administrator.')	
			return redirect(request.POST.get('work').replace('api/', ''))
	else:
		if request.user.is_authenticated:			
			response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/chapters/'+str(id))
			chapter = response.json()
			return render(request, 'chapter_form.html', {'chapter': chapter})
		else:
			messages.add_message(request, messages.ERROR, 'You must log in to perform this action.')	
			return redirect('/login')

def edit_work(request, id):
	if request.method == 'POST':
		work_dict = request.POST.copy()
		tags = []
		tag_types = {}
		result = requests.get(settings.ALLOWED_HOSTS[0] + '/api/tagtypes', cookies=request.COOKIES).json()['results']
		for item in result:
			tag_types[item['label']] = item
		for item in request.POST:
			dict_item = request.POST[item].replace('\'', '"')
			if 'tag_type_id' in request.POST[item]:				
				json_item = json.loads(dict_item)
				if not json_item['tag_type']:
					json_item['tag_type'] = tag_types[json_item['tag_type']]['url']
				tags.append(json_item)
				work_dict.pop(item)
			elif 'tag_type' in request.POST[item]:				
				json_item = json.loads(dict_item)
				if not json_item['tag_type']:
					json_item['tag_type'] = tag_types[json_item['tag_type']]['url']
				tags.append(json_item)
				work_dict.pop(item)
		work_dict["tags"] = tags
		comments_permitted = work_dict["comments_permitted"]
		work_dict["comments_permitted"] = comments_permitted == "All" or comments_permitted == "Registered users only"
		work_dict["anon_comments_permitted"] = comments_permitted == "All"
		work_dict = work_dict.dict()
		work_dict["user"] = str(request.user)
		work_json = json.dumps(work_dict)
		headers = {}
		headers['X-CSRFToken'] = request.COOKIES['csrftoken']
		headers['content-type'] = 'application/json'
		if id > 0:
			response = requests.put(settings.ALLOWED_HOSTS[0] + '/api/works/' + str(id) +'/', data=work_json, cookies=request.COOKIES, headers=headers)
			if response.status_code == 200:
				messages.add_message(request, messages.SUCCESS, 'Work updated.')	
			elif response.status_code == 403:
				messages.add_message(request, messages.ERROR, 'You are not authorized to update this work.')	
			else:
				messages.add_message(request, messages.ERROR, 'An error has occurred while updating this work. Please contact your administrator.')	
			return redirect('/works/'+str(id))
		else:
			response = requests.post(settings.ALLOWED_HOSTS[0] + '/api/works/', data=work_json, cookies=request.COOKIES, headers=headers)
			if response.status_code == 201:
				messages.add_message(request, messages.SUCCESS, 'Work created.')	
				response_json = response.json()
				new_id = response_json['id']
				return redirect('/works/'+str(new_id))
			elif response.status_code == 403:
				messages.add_message(request, messages.ERROR, 'You are not authorized to create this work.')	
				return redirect('/works/new')
			else:
				messages.add_message(request, messages.ERROR, 'An error has occurred while creating this work. Please contact your administrator.')	
				return redirect('/works/new')	
	else:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes', cookies=request.COOKIES)
		work_types = response.json()
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/tagtypes')
		tag_types = response.json()
		if request.user.is_authenticated:
			response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/'+str(id))
			work = response.json()
			tags = group_tags(tag_types['results'], work['tags'])
			return render(request, 'work_form.html', {'work_types': work_types['results'],
				'work': work, 
				'tags': tags})
		else:
			messages.add_message(request, messages.ERROR, 'You must log in to perform this action.')	
			return redirect('/login')

def log_in(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		if user is not None:
			login(request, user)
			messages.add_message(request, messages.SUCCESS, 'Login successful.')		
			return redirect(request.POST.get('referrer'))
		else:
			messages.add_message(request, messages.ERROR, 'Login unsuccessful. Please try again.')
			return redirect('/login')
	else:
		if 'HTTP_REFERER' in request.META:
			return render(request, 'login.html', {'referrer': request.META['HTTP_REFERER']})
		else:
			return render(request, 'login.html', {'referrer': '/'})

def register(request):
	if request.method == 'POST':
		headers = {}
		headers['X-CSRFToken'] = request.COOKIES['csrftoken']
		headers['content-type'] = 'application/json'
		user_data = json.dumps(request.POST)
		response = requests.post(settings.ALLOWED_HOSTS[0] + '/api/users/', data=user_data, cookies=request.COOKIES, headers=headers)
		if response.status_code == 200:
			messages.add_message(request, messages.SUCCESS, 'Registration successful!')		
			return redirect('/')
		elif response.status_code == 403:
			messages.add_message(request, messages.ERROR, 'Registration is not permitted at this time. Please contact site admin.')				
			return redirect('/')
		else:
			messages.add_message(request, messages.ERROR, 'Registration unsuccessful. Please try again.')
			return redirect('/login')
	else:			
		return render(request, 'register.html', {})

def log_out(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'Logout successful.')		
	return redirect(request.META['HTTP_REFERER'])


@require_http_methods(["GET"])
def work(request, pk):
	chapter_offset = int(request.GET.get('offset', 0))
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/'+str(pk))
	work = response.json()
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/tagtypes')
	tag_types = response.json()
	tags = group_tags(tag_types['results'], work['tags']) if 'tags' in work else {}
	if chapter_offset == 0:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/'+str(pk)+'/chapters?limit=1')
	else:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/'+str(pk)+'/chapters?limit=1&offset='+str(chapter_offset))
	response = response.json()
	chapter = response['results'][0] if 'results' in response and len(response['results']) > 0 else {}
	return render(request, 'work.html', {'work_types': work_types['results'], 
		'work': work,
		'id': pk,
		'tags': tags,
		'root': settings.ALLOWED_HOSTS[0],
		'chapter': chapter,
		'next_chapter': settings.ALLOWED_HOSTS[0] + '/works/'+str(pk)+'?offset='+str(chapter_offset + 1) if 'next' in response and response['next'] else None,
		'previous_chapter': settings.ALLOWED_HOSTS[0] + '/works/'+str(pk)+'?offset='+str(chapter_offset - 1)  if 'previous' in response and response['previous'] else None,})

def bookmarks(request):	
	return render(request, 'bookmarks.html', {})

def bookmark(request, pk):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/bookmarks/'+str(pk))
	bookmark = response.json()
	response = requests.get(bookmark['work'])
	work = response.json()
	return render(request, 'bookmark.html', {'bookmark': bookmark, 'work': work})

def upload_file(request):
	if request.method == 'POST':
		# todo
		# send fic uuid + chapter id
		# directory structure: media/uuid/chapter_id/files
		# save file, return location
		# location client-side in audio_url variable
		file_helpers.handle_uploaded_file(request.FILES['files[]'], request.FILES['files[]'].name)
		return redirect('/')
	return render(request, 'upload.html')
