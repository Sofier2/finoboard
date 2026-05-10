from django.urls import path
from . import views
from .views import change_request_status

urlpatterns = [
    path('', views.home, name='home'),

    path('create/', views.create_request, name='create'),
    path('requests/', views.list_requests, name='list'),
    path('vote/<int:request_id>/', views.vote, name='vote'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('my-requests/', views.my_requests, name='my_requests'),
    path('delete/<int:id>/', views.delete_request, name='delete_request'),


    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('supervisor-dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('edit/<int:id>/', views.edit_request, name='edit_request'),
    path(
    'hardware-login/',
    views.hardware_login,
    name='hardware_login'
),
path(
    'admin-delete/<int:id>/',
    views.admin_delete_request,
    name='admin_delete_request'
),
path('check-hardware-auth/', views.check_hardware_auth),

  path(
    'restore/<int:id>/',
    views.restore_request,
    name='restore_request'
),
path(
    'hard-delete/<int:id>/',
    views.hard_delete_request,
    name='hard_delete_request'
),
path('request/<int:pk>/status/', change_request_status, name='change_request_status'),
]