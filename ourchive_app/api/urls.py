from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework.routers import DefaultRouter




urlpatterns = [
	path('', views.api_root),
    path('works/', views.WorkList.as_view(), name='work-list'),
    path('works/<int:pk>/', views.WorkDetail.as_view(), name='work-detail'),
    path('chapters/', views.ChapterList.as_view(), name='chapter-list'),
    path('chapters/<int:pk>/', views.ChapterDetail.as_view(), name='chapter-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('tagtypes/', views.TagTypeList.as_view(), name='tag-type-list'),
    path('tagtypes/<int:pk>/', views.TagTypeDetail.as_view(), name='tagtype-detail'),
    path('tags/', views.TagList.as_view(), name='tag-list'),
    path('tags/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
	path('users/<int:pk>/',
        views.UserDetail.as_view(),
        name='user-detail'),
	path('works/<int:work_id>/chapters/<int:pk>', views.WorkChapters.as_view(), name='work-chapters'),
]


urlpatterns = format_suffix_patterns(urlpatterns)