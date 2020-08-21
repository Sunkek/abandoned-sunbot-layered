"""URL mapping.
Commented out router stuff because it messed up the PATCH request"""
from django.urls import include, path
# from django.conf.urls import include, url
# from rest_framework import routers
import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'messages', views.MessagesViewSet)

urlpatterns = [
    # path("", include(router.urls)),
    path("user/<int:user_id>/", views.user, name="user"),
    path("settings/<int:guild_id>/", views.settings, name="settings"),
    path("settings/", views.settings, name="settings"),

    path("birthdays/today", views.birthdays_today, name="birthdays_today"),

    path("messages/", views.messages, name="messages"),
    path("reactions/", views.reactions, name="reactions"),
    path("games/", views.games, name="games"),
    path("voice/", views.voice, name="voice"),
    path("emotes/", views.emotes, name="emotes"),
    path("nwords/", views.nwords, name="nwords"),

    path("top/postcounts/<str:time_range>/", views.top_postcounts, name="top_postcounts"),
    path("top/activity/<str:time_range>/", views.top_activity, name="top_activity"),
    path("top/emotes/<str:time_range>/", views.top_emotes, name="top_emotes"),
    path("top/nwords/<str:time_range>/", views.top_nwords, name="top_nwords"),
    
    path("active/<int:guild_id>/", views.active_members, name="active_members"),

    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]
