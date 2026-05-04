from django.urls import path
from . import views

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

    # 🔴 ДОДАЙ ОЦЕ
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('supervisor-dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('edit/<int:id>/', views.edit_request, name='edit_request'),
]