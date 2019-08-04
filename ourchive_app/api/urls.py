from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework.routers import DefaultRouter


work_list = views.WorkViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
work_detail = views.WorkViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

router = DefaultRouter()
router.register(r'works', views.WorkViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]