from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.response import Response

from datetime import date

from api.serializers import UserSerializer
from api.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, user_id, *args, **kwargs):
        try:
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
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
        

class BirthdaysTodayViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        birthdays = list(User.objects.all())
        birthdays = [
            i.user_id for i in birthdays 
            if i.birthday == date.today()
        ]
        return Response(birthdays)


"""Define the allowed request methods for each ModelViewSet"""
user = UserViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})
birthdays_today = BirthdaysTodayViewSet.as_view({
    'get': 'list',
})