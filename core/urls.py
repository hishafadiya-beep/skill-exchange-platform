from django.urls import path
from .views import register, login_view, dashboard, profile, logout_view, assessment, find_people

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('assessment/', assessment, name='assessment'),
    path('find-people/', find_people, name='find_people'),
]