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


def group_tags(tag_types, tags):
	result = {}
	for tag_type in tag_types:
		result[tag_type['label']] = []
	for tag in tags:
		result[tag['tag_type']].append(tag)
	return result

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
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/')
	works = response.json()['results']
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/tagtypes')
	tag_types = response.json()
	for work in works:
		tags = group_tags(tag_types['results'], work['tags']) if 'tags' in work else {}
		work['tags'] = tags
	return render(request, 'works.html', {
		'works': works,
		'root': settings.ALLOWED_HOSTS[0]})

def works_by_type(request, type_id):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes/'+str(type_id) + '/works')
	works = response.json()['results']
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/tagtypes')
	tag_types = response.json()
	for work in works:
		tags = group_tags(tag_types['results'], work['tags']) if 'tags' in work else {}
		work['tags'] = tags
	return render(request, 'works.html', {
		'works': works,
		'root': settings.ALLOWED_HOSTS[0]})

def new_work(request):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes')
	work_types = response.json()
	if request.user.is_authenticated and request.method != 'POST':
		headers = {}
		headers['X-CSRFToken'] = request.COOKIES['csrftoken']
		headers['content-type'] = 'application/json'
		response = requests.post(settings.ALLOWED_HOSTS[0] + '/api/works/', data=json.dumps({'title': 'Untitled Work', 'user': request.user.username}), cookies=request.COOKIES, headers=headers)
		if response.status_code == 201:
			messages.add_message(request, messages.SUCCESS, 'Work created.')	
			work = response.json()
			return render(request, 'work_form.html', {'work_types': work_types['results'],
			'work': work})
		elif response.status_code == 403:
			messages.add_message(request, messages.ERROR, 'You are not authorized to create this work.')	
			return redirect('/')
		else:
			messages.add_message(request, messages.ERROR, 'An error has occurred while creating this work. Please contact your administrator.')	
			print(response.json())
			return redirect('/')		
	elif request.user.is_authenticated:
		return edit_work(request, int(request.POST['work_id']))
	else:
		messages.add_message(request, messages.ERROR, 'You must log in to post a new work.')	
		return redirect('/login')



def new_chapter(request, work_id):
	if request.user.is_authenticated and request.method != 'POST':
		headers = {}
		headers['X-CSRFToken'] = request.COOKIES['csrftoken']
		headers['content-type'] = 'application/json'
		request_json = {'title': 'Untitled Chapter', 'work': work_id, 'text': '', 'number': int(request.GET.get('count', 1)) + 1}
		response = requests.post(settings.ALLOWED_HOSTS[0] + '/api/chapters/', data=json.dumps(request_json), cookies=request.COOKIES, headers=headers)
		if response.status_code == 201:
			messages.add_message(request, messages.SUCCESS, 'Chapter created.')	
			chapter = response.json()
			return render(request, 'chapter_form.html', {'chapter': chapter})
		elif response.status_code == 403:
			messages.add_message(request, messages.ERROR, 'You are not authorized to create this chapter.')	
			return redirect('/works/'+str(work_id))
		else:
			messages.add_message(request, messages.ERROR, 'An error has occurred while creating this chapter. Please contact your administrator.')	
			print(response.json())
			return redirect('/works/'+str(work_id))
	elif request.user.is_authenticated:
		return edit_chapter(request, work_id, request.POST['chapter_id'])
	else:
		messages.add_message(request, messages.ERROR, 'You must log in to post a new work.')	
		return redirect('/login')

def edit_chapter(request, work_id, id):
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
			return redirect('/works/'+str(work_id))
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
		chapters = []
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
			elif 'chapters_' in item:
				chapter_id = item[9:]
				chapter_number = request.POST[item]
				chapters.append({'id': chapter_id, 'number': chapter_number, 'work': id})
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
		response = requests.put(settings.ALLOWED_HOSTS[0] + '/api/works/' + str(id) +'/', data=work_json, cookies=request.COOKIES, headers=headers)
		if response.status_code == 200:
			for chapter in chapters:
				response = requests.put(settings.ALLOWED_HOSTS[0] + '/api/chapters/' + str(chapter['id']) +'/', data=json.dumps(chapter), cookies=request.COOKIES, headers=headers)
			messages.add_message(request, messages.SUCCESS, 'Work updated.')	
		elif response.status_code == 403:
			messages.add_message(request, messages.ERROR, 'You are not authorized to update this work.')	
		else:
			messages.add_message(request, messages.ERROR, 'An error has occurred while updating this work. Please contact your administrator.')	
		return redirect('/works/'+str(id))
			
	else:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/worktypes', cookies=request.COOKIES)
		work_types = response.json()
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/tagtypes')
		tag_types = response.json()
		if request.user.is_authenticated:
			response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/'+str(id))
			work = response.json()
			response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/works/'+str(id) + '/chapters')
			chapters = response.json()
			tags = group_tags(tag_types['results'], work['tags'])
			return render(request, 'work_form.html', {'work_types': work_types['results'],
				'work': work, 
				'tags': tags,
				'chapters': chapters['results'],
				'chapter_count': len(chapters)})
		else:
			messages.add_message(request, messages.ERROR, 'You must log in to perform this action.')	
			return redirect('/login')

def edit_bookmark(request, pk):
	if request.method == 'POST':
		bookmark_dict = request.POST.copy()
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
				bookmark_dict.pop(item)
			elif 'tag_type' in request.POST[item]:				
				json_item = json.loads(dict_item)
				if not json_item['tag_type']:
					json_item['tag_type'] = tag_types[json_item['tag_type']]['url']
				tags.append(json_item)
				bookmark_dict.pop(item)
		bookmark_dict["tags"] = tags
		#comments_permitted = bookmark_dict["comments_permitted"]
		#bookmark_dict["comments_permitted"] = comments_permitted == "All" or comments_permitted == "Registered users only"
		#bookmark_dict["anon_comments_permitted"] = comments_permitted == "All"
		bookmark_dict = bookmark_dict.dict()
		bookmark_dict["user"] = str(request.user)
		bookmark_dict["work_id"] = bookmark_dict["work"]
		bookmark_dict.pop("work")
		bookmark_json = json.dumps(bookmark_dict)
		headers = {}
		headers['X-CSRFToken'] = request.COOKIES['csrftoken']
		headers['content-type'] = 'application/json'
		response = requests.put(settings.ALLOWED_HOSTS[0] + '/api/bookmarks/' + str(pk) +'/', data=bookmark_json, cookies=request.COOKIES, headers=headers)
		if response.status_code == 200:			
			messages.add_message(request, messages.SUCCESS, 'Bookmark updated.')	
		elif response.status_code == 403:
			messages.add_message(request, messages.ERROR, 'You are not authorized to update this bookmark.')	
		else:
			print(response.content)
			messages.add_message(request, messages.ERROR, 'An error has occurred while updating this bookmark. Please contact your administrator.')	
		return redirect('/bookmarks/'+str(pk))
			
	else:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/tagtypes')
		tag_types = response.json()
		if request.user.is_authenticated:
			response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/bookmarks/'+str(pk))
			bookmark = response.json()
			tags = group_tags(tag_types['results'], bookmark['tags'])
			return render(request, 'bookmark_form.html', {
				'bookmark': bookmark, 
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
	chapter_response = response.json()
	chapter = chapter_response['results'][0] if 'results' in chapter_response and len(chapter_response['results']) > 0 else {}
	if 'id' in chapter:
		response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/chapters/'+str(chapter['id'])+'/comments')
		comments = response.json()
	else:
		comments = []
	return render(request, 'work.html', {'work_types': work_types['results'], 
		'work': work,
		'comments': comments,
		'id': pk,
		'tags': tags,
		'root': settings.ALLOWED_HOSTS[0],
		'chapter': chapter,
		'next_chapter': settings.ALLOWED_HOSTS[0] + '/works/'+str(pk)+'?offset='+str(chapter_offset + 1) if 'next' in chapter_response and chapter_response['next'] else None,
		'previous_chapter': settings.ALLOWED_HOSTS[0] + '/works/'+str(pk)+'?offset='+str(chapter_offset - 1)  if 'previous' in chapter_response and chapter_response['previous'] else None,})

def render_comments(request, chapter_id):
	next_url = request.GET.get('next', '')
	offset_url = request.GET.get('offset', '')
	response = requests.get(next_url+"&offset="+offset_url)
	comments = response.json()
	return render(request, 'comments.html', {'comments': comments, 'chapter': {'id': chapter_id}})

def create_chapter_comment(request, work_id, chapter_id):
	if request.method == 'POST':
		comment_dict = request.POST.copy()
		comment_dict["user"] = str(request.user)
		comment_json = json.dumps(comment_dict)
		headers = {}
		headers['X-CSRFToken'] = request.COOKIES['csrftoken']
		headers['content-type'] = 'application/json'
		response = requests.post(settings.ALLOWED_HOSTS[0] + '/api/comments/', data=comment_json, cookies=request.COOKIES, headers=headers)
		if response.status_code == 200:
			messages.add_message(request, messages.SUCCESS, 'Comment posted.')	
		elif response.status_code == 201:
			messages.add_message(request, messages.SUCCESS, 'Comment posted.')	
		elif response.status_code == 403:
			messages.add_message(request, messages.ERROR, 'You are not authorized to post this comment.')	
		else:
			messages.add_message(request, messages.ERROR, 'An error has occurred while posting this comment. Please contact your administrator.')	
		return redirect('/works/'+str(work_id))

def bookmarks(request):	
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/bookmarks/')
	bookmarks = response.json()['results']
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/tagtypes')
	tag_types = response.json()
	for bookmark in bookmarks:
		print(bookmark)
		tags = group_tags(tag_types['results'], bookmark['tags']) if 'tags' in bookmark else {}
		bookmark['tags'] = tags
	return render(request, 'bookmarks.html', {'bookmarks': bookmarks})

def bookmark(request, pk):
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/bookmarks/'+str(pk))
	bookmark = response.json()
	response = requests.get(settings.ALLOWED_HOSTS[0] + '/api/bookmarks/'+str(pk)+'/comments')
	comments = response.json()
	return render(request, 'bookmark.html', {'bookmark': bookmark, 'work': bookmark['work'] if 'work' in bookmark else {}, 'comments': comments})

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
