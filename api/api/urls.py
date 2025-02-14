from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('merga_123334/', admin.site.urls),
    path('kehelot_ai/', include('kehelot_ai.urls')), 
]
