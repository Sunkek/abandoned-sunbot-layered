"""URL mapping.
Commented out router stuff because it messed up the PATCH request"""
from django.urls import include, path
# from django.conf.urls import include, url
# from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'messages', views.MessagesViewSet)

urlpatterns = [
    # path("", include(router.urls)),
    path("user/<int:user_id>/", views.user, name="user"),
    # path("users/", views.users, name="user"),
    path("settings/<int:guild_id>/", views.settings, name="settings"),
    path("settings/", views.settings, name="settings"),
    path("birthdays/today", views.birthdays_today, name="birthdays_today"),
    path("messages/", views.messages, name="messages"),
    path("reactions/", views.reactions, name="reactions"),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]
