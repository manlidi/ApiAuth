# accounts/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('update_user/', update_user, name='update_user'),
    
    path('books/', allBooks, name='books'),
    path('book/<int:id>/', getbooks, name='book'),
    path('addbooks/', addbooks, name='addbooks'),
    path('editbooks/<int:id>/', editbooks, name='editbooks'),
    path('del/<int:id>/', deletebooks, name='del'),
]