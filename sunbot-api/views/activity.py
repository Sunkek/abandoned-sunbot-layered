from django.db.utils import IntegrityError
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, pagination
from rest_framework.response import Response

from api.serializers import ActivitySerializer, ActivityTopSerializer
from api.pagination import CustomPageNumberPagination
from api.models import User, Guild, Activity


class TopActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = CustomPageNumberPagination
    

    def list(self, request, time_range, *args, **kwargs):
        data = request.data
        activities = Activity.objects
        if data["guild_id"]:  # Top for the guild
            activities = activities.filter(guild_id=data["guild_id"])
        activities = activities.values("user_id").annotate(
            count=Sum("activity")
        ).order_by("-count")
        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = ActivityTopSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ActivityTopSerializer(activities, many=True)
        # Add activity points
        return Response(serializer.data)


"""Define the allowed request methods for each ModelViewSet"""
top_activity = TopActivityViewSet.as_view({
    'get': 'list',
})