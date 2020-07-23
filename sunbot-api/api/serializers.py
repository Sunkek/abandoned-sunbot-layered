from rest_framework import serializers, pagination
from rest_framework.response import Response

from .models import User, Guild, Messages, Reactions, Games, Voice, Emotes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = "__all__"


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        exclude = ["id"]  # Useless primary key field
        
class MessagesTopSerializer(serializers.ModelSerializer):
    sum_postcount = serializers.IntegerField()
    user_id = serializers.IntegerField()
    
    class Meta:
        model = Messages
        fields = ["user_id", "sum_postcount"]


class ReactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reactions
        exclude = ["id"]  # Useless primary key field


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        exclude = ["id"]  # Useless primary key field


class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voice
        exclude = ["id"]  # Useless primary key field


class EmotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotes
        exclude = ["id"]  # Useless primary key field


class CustomPageNumberPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data, total):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "current": self.self.page.number,
            "last": self.page.paginator.num_pages,
            "count": self.page.paginator.count,
            "total": self.total,
            "results": data,
        })