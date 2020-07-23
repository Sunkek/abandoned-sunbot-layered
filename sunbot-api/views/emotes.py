from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import EmotesSerializer
from api.models import User, Guild, Emotes


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


"""Define the allowed request methods for each ModelViewSet"""
emotes = EmotesViewSet.as_view({
    'patch': 'partial_update',
})