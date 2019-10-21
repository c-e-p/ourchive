from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index),
    path('search/', views.search),
    path('works/', views.works),
    path('works/new', views.new_work),
    path('works/<int:id>/edit', views.edit_work),
    path('works/type/<int:type_id>', views.works_by_type),
    path('works/<int:pk>/', views.work),
    path('bookmarks/', views.bookmarks),
    path('bookmark/<int:pk>/', views.bookmark),
]