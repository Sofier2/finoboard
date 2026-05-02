from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔥 всі сторінки тепер тут
    path('', include('requests_app.urls')),
]