from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    # Remove this line for now: path('api/', include('api.urls')),
]