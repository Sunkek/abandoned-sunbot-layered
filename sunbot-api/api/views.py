from django.shortcuts import render
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from datetime import datetime

from .serializers import UserSerializer, GuildSerializer, MessagesSerializer
from .models import User, Guild, Messages


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, user_id, *args, **kwargs):
        try:
            # Find the existing user entry
            user = User.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            user = User(user_id=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def partial_update(self, request, user_id, *args, **kwargs):
        """PATCH requests fall here.
        Here I'm working from the idea that the entry already exists,
        so I just find it and update. Only if it doesn't exist,
        I create a new one and save it."""
        data = request.data
        try:
            # Find the existing user entry
            user = User.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            # Entry not found - create one!
            user = User(user_id=user_id)
        # Update kwargs
        for key, value in data.items():
            if value == "reset":
                value = None
            setattr(user, key, value)
        # Submit changes
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

    def partial_update(self, request, *args, **kwargs):
        """PATCH requests fall here.
        Here I'm working from the idea that the entry already exists,
        so I just find it and update the counters. Only if it doesn't exist,
        I create a new one and try to save it. If it can't save because
        there's no member in the database, I create that member."""
        data = request.data
        try:
            # Find the existing message entry
            messages = Messages.objects.get(
                guild_id=data["guild_id"],
                channel_id=data["channel_id"],
                user_id=User(user_id=data["user_id"]),
                period=data["period"][:-2]+"01",  # The first of the current month
            )
        except ObjectDoesNotExist:
            # Entry not found - create one!
            messages = Messages(
                guild_id=data["guild_id"],
                channel_id=data["channel_id"],
                user_id=User(user_id=data["user_id"]),
                period=data["period"][:-2]+"01",  # The first of the current month
            )
        # Update counters
        messages.postcount += data["postcount"]
        messages.attachments += data["attachments"]
        messages.words += data["words"]
        try:
            # Submit changes
            messages.save()
        except IntegrityError:
            # If there's no member - create one!
            author = User(user_id=request.data["user_id"])
            author.save()
            messages.save()
        serializer = self.get_serializer(messages)
        return Response(serializer.data)


class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Guild.objects.all()
    serializer_class = GuildSerializer

    def list(self, request, *args, **kwargs):
        settings = list(Guild.objects.all().values())
        settings = {
            i.pop("guild_id"): i for i in settings
        }
        print(settings)
        return Response(settings)

    def partial_update(self, request, guild_id, *args, **kwargs):
        """PATCH requests fall here.
        Here I'm working from the idea that the entry already exists,
        so I just find it and update. Only if it doesn't exist,
        I create a new one and save it."""
        data = request.data
        try:
            # Find the existing guild entry
            guild = Guild.objects.get(guild_id=guild_id)
        except ObjectDoesNotExist:
            # Entry not found - create one!
            guild = Guild(guild_id=guild_id)
        # Update kwargs
        for key, value in data.items():
            print(key, value)
            if value == "reset": value = None
            setattr(guild, key, value)
        # Submit changes
        guild.save()
        serializer = self.get_serializer(guild)
        return Response(serializer.data)


class BirthdaysTodayViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        birthdays = list(User.objects.all())

        birthdays = [
            i.user_id for i in birthdays 
            if i.birthday == datetime.date.today()
        ]
        return Response(birthdays)


"""Define the allowed request methods for each ModelViewSet"""
user = UserViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})
messages = MessagesViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})
settings = SettingsViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})
birthdays_today = BirthdaysTodayViewSet.as_view({
    'get': 'list',
})
