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
    review_user,
    learning_queries,
    post_learning_query,
    mark_query_solved,
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
        path('learning-queries/', learning_queries, name='learning_queries'),
        path('post-query/', post_learning_query, name='post_learning_query'),
        path(
            'learning-queries/<int:query_id>/solved/',
            mark_query_solved,
            name='mark_query_solved'
),
]