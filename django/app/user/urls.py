from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('list/', views.ListUserView.as_view(), name='list'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
