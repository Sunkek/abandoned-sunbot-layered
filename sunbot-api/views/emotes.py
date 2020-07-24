from django.db.utils import IntegrityError
from django.db.models import Sum
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import EmotesSerializer, EmotesTopSerializer
from api.pagination import CustomPageNumberPagination
from api.models import User, Guild, Emotes, Reactions


class EmotesViewSet(viewsets.ModelViewSet):
    queryset = Emotes.objects.all()
    serializer_class = EmotesSerializer

    def partial_update(self, request, *args, **kwargs):
        """PATCH requests fall here.
        Here I'm working from the idea that the entry already exists,
        so I just find it and update the counters. Only if it doesn't exist,
        I create a new one and try to save it. If it can't save because
        there's no member in the database, I create that member."""
        data = request.data
        try:
            # Find the existing message entry
            emotes = Emotes.objects.get(
                guild_id=Guild(guild_id=data["guild_id"]),
                user_id=User(user_id=data["user_id"]),
                emote=data["emote"],
                period=data["period"][:-2]+"01",  # The first of the current month
            )
        except ObjectDoesNotExist as e:
            # Entry not found - create one!
            emotes = Emotes(
                guild_id=Guild(guild_id=data["guild_id"]),
                user_id=User(user_id=data["user_id"]),
                emote=data["emote"],
                period=data["period"][:-2]+"01",  # The first of the current month
            )
        # Update counters
        emotes.count += data["count"]
        try:
            # Submit changes
            emotes.save()
        except IntegrityError as e:
            # If there's no member - create one!
            if "user_id" in str(e.__cause__):
                user = User(user_id=data["user_id"])
                user.save()
            else: raise e
            emotes.save()
        serializer = self.get_serializer(emotes)
        return Response(serializer.data)


class TopEmotesViewSet(viewsets.ModelViewSet):
    queryset = Emotes.objects.all()
    serializer_class = EmotesSerializer
    pagination_class = CustomPageNumberPagination
    
    def list(self, request, time_range, *args, **kwargs):
        try:
            data = request.data

            cursor = connection.cursor()
            cursor.execute(
                "SELECT CASE WHEN emotes.emote IS NULL THEN reactions.emote "
                "ELSE emotes.emote END as emote, "
                "sum(emotes.count) as message_count, "
                "sum(reactions.count) as reaction_count, "
                "sum(emotes.count)+sum(reactions.count) as total_count "
                "FROM emotes JOIN reactions ON (emotes.emote = reactions.emote "
                "AND emotes.period = reactions.period AND "
                "emotes.guild_id = reactions.guild_id) "
                f"WHERE emotes.guild_id={data['guild_id']} OR "
                f"reactions.guild_id={data['guild_id']} "
                "GROUP BY emotes.emote, reactions.emote ORDER BY total_count DESC"
            )
            print(cursor)
            page = self.paginate_queryset(cursor)
            if page is not None:
                serializer = EmotesTopSerializer(cursor, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = EmotesTopSerializer(cursor, many=True)
            cursor.close()
            return Response(serializer.data)
        except Exception as e: 
            print(e)


"""Define the allowed request methods for each ModelViewSet"""
emotes = EmotesViewSet.as_view({
    'patch': 'partial_update',
})
top_emotes = TopEmotesViewSet.as_view({
    'get': 'list',
})