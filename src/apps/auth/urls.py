from django.urls import path

from .views import Login, Logout, AuthMe

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('me', AuthMe.as_view(), name='auth_me'),
]
