from django.urls import path
from .views import (home_view,tweet_list_view,tweet_detail_view,
tweet_create_view,tweet_create_view_pure_django,tweet_delete_view,tweet_action_view)

app_name = 'tweet'
'''
REST API BUILT WITH BASE ENDPOINT /api/tweets
'''

urlpatterns = [
    path('create/', tweet_create_view,name='create'),
    path('',tweet_list_view,name='tweetlist'),
     path('<int:tweet_id>/', tweet_detail_view,name='detail'),
    path('action/', tweet_action_view,name='tweet-action'),
     path('<int:tweet_id>/delete',tweet_delete_view,name='delete')
]