from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import ReactionsSerializer
from api.models import User, Guild, Reactions


class ReactionsViewSet(viewsets.ModelViewSet):
    queryset = Reactions.objects.all()
    serializer_class = ReactionsSerializer

    def partial_update(self, request, *args, **kwargs):
        """PATCH requests fall here.
        Here I'm working from the idea that the entry already exists,
        so I just find it and update the counters. Only if it doesn't exist,
        I create a new one and try to save it. If it can't save because
        there's no member in the database, I create that member."""
        data = request.data
        try:
            # Find the existing message entry
            reactions = Reactions.objects.get(
                guild_id=Guild(guild_id=data["guild_id"]),
                giver_id=User(user_id=data["giver_id"]),
                receiver_id=User(user_id=data["receiver_id"]),
                emote=data["emote"],
                period=data["period"][:-2]+"01",  # The first of the current month
            )
        except ObjectDoesNotExist as e:
            # Entry not found - create one!
            reactions = Reactions(
                guild_id=Guild(guild_id=data["guild_id"]),
                giver_id=User(user_id=data["giver_id"]),
                receiver_id=User(user_id=data["receiver_id"]),
                emote=data["emote"],
                period=data["period"][:-2]+"01",  # The first of the current month
            )
        # Update counters
        reactions.count += data["count"]
        try:
            # Submit changes
            reactions.save()
        except IntegrityError as e:
            # If there's no member - create one!
            if "giver_id" in str(e.__cause__):
                giver = User(user_id=data["giver_id"])
                giver.save()
            elif "receiver_id" in str(e.__cause__):
                receiver = User(user_id=data["receiver_id"])
                receiver.save()
            else: raise e
            try:
                reactions.save()
            except IntegrityError as e:
                if "receiver_id" in str(e.__cause__):
                    receiver = User(user_id=data["receiver_id"])
                    receiver.save()
                else: raise e
                reactions.save()
        serializer = self.get_serializer(reactions)
        return Response(serializer.data)

"""Define the allowed request methods for each ModelViewSet"""
reactions = ReactionsViewSet.as_view({
    'patch': 'partial_update',
})