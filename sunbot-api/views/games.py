from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import GamesSerializer
from api.models import User, Games


class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer

    def partial_update(self, request, *args, **kwargs):
        """PATCH requests fall here.
        Here I'm working from the idea that the entry already exists,
        so I just find it and update the counters. Only if it doesn't exist,
        I create a new one and try to save it. If it can't save because
        there's no member in the database, I create that member."""
        data = request.data
        try:
            # Find the existing message entry
            game = Games.objects.get(
                user_id=User(user_id=data["user_id"]),
                game=data["game"],
                period=data["period"][:-2]+"01",  # The first of the current month
            )
        except ObjectDoesNotExist as e:
            # Entry not found - create one!
            game = Games(
                user_id=User(user_id=data["user_id"]),
                game=data["game"],
                period=data["period"][:-2]+"01",  # The first of the current month
            )
        # Update counters
        game.duration += data["duration"]
        try:
            # Submit changes
            game.save()
        except IntegrityError as e:
            # If there's no member - create one!
            if "user_id" in str(e.__cause__):
                user = User(user_id=data["user_id"])
                user.save()
            else: raise e
            game.save()
        serializer = self.get_serializer(game)
        return Response(serializer.data)

"""Define the allowed request methods for each ModelViewSet"""
games = GamesViewSet.as_view({
    'patch': 'partial_update',
})