from django.urls import path
from .views import (
    register,
    login_view,
    dashboard,
    profile,
    logout_view,
    assessment,
    find_people,
    send_exchange_request,
    exchange_requests,
    chat,
    review_user
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),

    # My profile
    path('profile/', profile, name='profile'),

    # View another user's profile
    path('profile/<int:user_id>/', profile, name='user_profile'),

    path('logout/', logout_view, name='logout'),
    path(
    'assessment/<int:skill_id>/',
    assessment,
    name='assessment'
),
    path('find-people/', find_people, name='find_people'),

    path(
    'send-request/<int:user_id>/<int:skill_id>/',
    send_exchange_request,
    name='send_exchange_request'),
    path(
    'exchange-requests/',
    exchange_requests,
    name='exchange_requests'),
        path(
        'chat/<int:user_id>/',
        chat,
        name='chat'
    ),

        path(
        'review/<int:user_id>/',
        review_user,
        name='review_user'
    ),
]