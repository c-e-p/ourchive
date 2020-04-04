from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', views.index),
    path('search/', views.search),
    path('works/', views.works),
    path('works/new', views.new_work),
    path('works/<int:id>/edit', views.edit_work),
    path('works/type/<int:type_id>', views.works_by_type),
    path('works/<int:pk>/', views.work),
    path('bookmarks/', views.bookmarks),
    path('bookmarks/<int:pk>/', views.bookmark),
    path('bookmarks/<int:pk>/comments', views.render_bookmark_comments),
    path('bookmarks/<int:pk>/comments/new', views.create_bookmark_comment),
    path('bookmarks/<int:pk>/comments/<int:comment_id>/edit', views.edit_bookmark_comment),
    path('bookmarks/<int:pk>/comments/<int:comment_id>/delete', views.delete_bookmark_comment),
    path('bookmarks/<int:pk>/edit', views.edit_bookmark),
    path('login/', views.log_in),
    path('register/', views.register),
    path('logout/', views.log_out),
    path('username/<str:username>', views.user_name),
    path('works/<int:work_id>/chapters/<int:id>/edit', views.edit_chapter),
    path('works/<int:work_id>/chapters/new', views.new_chapter),
    path('works/<int:work_id>/chapters/<int:chapter_id>/comments', views.render_comments),
    path('works/<int:work_id>/chapters/<int:chapter_id>/comments/new', views.create_chapter_comment),
    path('works/<int:work_id>/chapters/<int:chapter_id>/comments/<int:comment_id>/edit', views.edit_chapter_comment),
    path('works/<int:work_id>/chapters/<int:chapter_id>/comments/<int:comment_id>/delete', views.delete_chapter_comment),
    path('upload-test', views.upload_file)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)