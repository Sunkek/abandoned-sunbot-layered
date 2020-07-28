from django.db.utils import IntegrityError
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, pagination
from rest_framework.response import Response

from api.serializers import MessagesSerializer, MessagesTopSerializer
from api.pagination import CustomPageNumberPagination
from api.models import User, Guild, Messages

from views import helpers


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
                guild_id=Guild(guild_id=data["guild_id"]),
                channel_id=data["channel_id"],
                user_id=User(user_id=data["user_id"]),
                period=data["period"][:-2]+"01",  # The first of the current month
            )
        except ObjectDoesNotExist:
            # Entry not found - create one!
            messages = Messages(
                guild_id=Guild(guild_id=data["guild_id"]),
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
            author = User(user_id=data["user_id"])
            author.save()
            messages.save()
        serializer = self.get_serializer(messages)
        return Response(serializer.data)


class TopPostcountsViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_paginated_response(self, data, total):
        """
        Return a paginated style `Response` object for the given output data.
        I just want to add total to my results.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, total)

    def list(self, request, time_range, *args, **kwargs):
        data = request.data
        messages = Messages.objects
        if data["channel_id"]:  #  Top for the channel
            messages = messages.filter(channel_id=data["channel_id"])
            total = Messages.objects.aggregate(total=Sum("postcount"))["total"]
        elif data["guild_id"]:  # Top for the guild
            messages = messages.filter(guild_id=data["guild_id"])
            total = Messages.objects.aggregate(total=Sum("postcount"))["total"]
        messages = messages.values("user_id").annotate(
            count=Sum("postcount")
        ).order_by("-count")
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessagesTopSerializer(page, many=True)
            return self.get_paginated_response(serializer.data, total)
        serializer = MessagesTopSerializer(messages, many=True)
        # Add activity points
        helpers.add_message_activity(data, Guild.objects.get(data["guild_id"]))
        return Response(serializer.data)


"""Define the allowed request methods for each ModelViewSet"""
messages = MessagesViewSet.as_view({
    'patch': 'partial_update',
})
top_postcounts = TopPostcountsViewSet.as_view({
    'get': 'list',
})