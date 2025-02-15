from django.contrib import admin
from django.urls import path, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('merga_123334/', admin.site.urls),
    path('kehelot_ai/', include('kehelot_ai.urls')), 
]

# urlpatterns += staticfiles_urlpatterns()
