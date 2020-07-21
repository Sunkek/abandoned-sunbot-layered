from rest_framework import serializers

from .models import User, Guild, Messages, Reactions, Games, Voice


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

