from django.shortcuts import render
from django.db.utils import IntegrityError

from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from .serializers import UserSerializer, MessagesSerializer
from .models import User, Messages

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
                server_id=data["server_id"],
                channel_id=data["channel_id"],
                member_id=User(member_id=data["member_id"]),
                period=data["period"][:-2]+"01", # The first of the current month
            )
        except Messages.DoesNotExist:
            # Entry not found - create one!
            messages = Messages(
                server_id=data["server_id"],
                channel_id=data["channel_id"],
                member_id=User(member_id=data["member_id"]),
                period=data["period"][:-2]+"01", # The first of the current month
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
            author = User(member_id=request.data["member_id"])
            author.save()
            messages.save()
        serializer = self.get_serializer(messages)
        return Response(serializer.data)

"""Define the allowed request methods for each ModelViewSet"""
users = UserViewSet.as_view({
    'get': 'list',
})
messages = MessagesViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})