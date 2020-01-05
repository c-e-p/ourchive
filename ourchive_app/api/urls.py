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
    path('works/<int:work_id>/chapters/', views.WorkChapterDetail.as_view(), name='work-chapter-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('tagtypes/', views.TagTypeList.as_view(), name='tag-type-list'),
    path('tagtypes/<int:pk>/', views.TagTypeDetail.as_view(), name='tagtype-detail'),
    path('worktypes/', views.WorkTypeList.as_view(), name='work-type-list'),
    path('worktypes/<int:pk>/', views.WorkTypeDetail.as_view(), name='worktype-detail'),
    path('worktypes/<int:type_id>/works', views.WorkByTypeList.as_view(), name='work-by-type-list'),
    path('tags/', views.TagList.as_view(), name='tag-list'),
    path('tags/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
    path('bookmarks/', views.BookmarkList.as_view(), name='bookmark-list'),
    path('bookmarks/<int:pk>/', views.BookmarkDetail.as_view(), name='bookmark-detail'),
    path('bookmarkcollections/', views.BookmarkCollectionList.as_view(), name='bookmark-collection-list'),
    path('bookmarkcollections/<int:pk>/', views.BookmarkCollectionDetail.as_view(), name='bookmarkcollection-detail'),
    path('comments/', views.CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
    path('messages/', views.MessageList.as_view(), name='message-list'),
    path('messages/<int:pk>/', views.MessageDetail.as_view(), name='message-detail'),
    path('notifications/', views.NotificationList.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationDetail.as_view(), name='notification-detail'),
    path('notificationtypes/', views.NotificationTypeList.as_view(), name='notification-type-list'),
    path('notificationtypes/<int:pk>/', views.NotificationTypeDetail.as_view(), name='notificationtype-detail'),
    path('settings/', views.OurchiveSettingList.as_view(), name='ourchive-setting-list'),
    path('settings/<int:pk>/', views.OurchiveSettingDetail.as_view(), name='ourchivesetting-detail'),
	path('users/<int:pk>/',
        views.UserDetail.as_view(),
        name='user-detail'),
    path('users/<str:username>/', views.UserNameDetail.as_view(),
        name='user-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)