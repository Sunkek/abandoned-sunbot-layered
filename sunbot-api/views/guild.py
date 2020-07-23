from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.response import Response

from datetime import date

from api.serializers import GuildSerializer
from api.models import Guild


class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Guild.objects.all()
    serializer_class = GuildSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        settings = list(Guild.objects.all().values())
        settings = {
            i.pop("guild_id"): i for i in settings
        }
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

"""Define the allowed request methods for each ModelViewSet"""
settings = SettingsViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})