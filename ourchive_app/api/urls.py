from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('works/', views.WorkList.as_view()),
    path('works/<int:pk>/', views.WorkDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)