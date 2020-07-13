"""URL mapping.
Commented out router stuff because it messed up the PATCH request"""
from django.urls import include, path
from django.conf.urls import url, include
#from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'messages', views.MessagesViewSet)

urlpatterns = [
    #path("", include(router.urls)),
    url(r"^users/$", views.users, name="user"),
    url(r"^messages/$", views.messages, name="messages"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]