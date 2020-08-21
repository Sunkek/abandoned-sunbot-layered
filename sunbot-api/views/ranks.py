from django.db.utils import IntegrityError
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, pagination
from rest_framework.response import Response

from api.serializers import ActivitySerializer, ActivityTopSerializer
from api.pagination import CustomPageNumberPagination
from api.models import Guild, Activity

from datetime import datetime


class ActiveMembersViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = None
    

    def list(self, request, guild_id, *args, **kwargs):
        # Get active role requirements
        try:
            settings = Guild.objects.get(guild_id=guild_id)
            req_activity = settings.rank_active_member_required_activity
            if not req_activity:
                return Response([])
            date = datetime.today().replace(month=datetime.now().month, day=1)
            active_members = Activity.objects.filter(
                guild_id=guild_id, activity__gte=req_activity, period=date,
            ).values_list("user_id", flat=True)
            print(active_members)
            return Response(active_members)
        except Exception as e:
            print(e)


"""Define the allowed request methods for each ModelViewSet"""
active_members = ActiveMembersViewSet.as_view({
    'get': 'list',
})