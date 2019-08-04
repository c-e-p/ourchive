from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('works/', views.WorkList.as_view()),
    path('works/<int:pk>/', views.WorkDetail.as_view(), name='work-detail'),
    path('users/', views.UserList.as_view()),
	path('users/<int:pk>/',
        views.UserDetail.as_view(),
        name='user-detail'),
	path('works/<int:pk>/chapters/', views.WorkChapters.as_view(), name='chapter-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)