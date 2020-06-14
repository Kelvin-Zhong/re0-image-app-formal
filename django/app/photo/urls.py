from django.urls import path, include
from rest_framework.routers import DefaultRouter

from photo import views

router = DefaultRouter()
router.register('photo', views.PhotoViewSet)

app_name = 'photo'

urlpatterns = [
    path('', include(router.urls))
]
