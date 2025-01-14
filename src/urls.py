from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth/', include('src.apps.auth.urls')),
        path('user/', include('src.apps.users.api.urls')),
        path('category/', include('src.apps.categories.api.urls')),
        path('product/', include('src.apps.products.api.urls')),
    
    ])),
]
