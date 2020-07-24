from rest_framework import serializers, pagination

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
    count = serializers.IntegerField()
    user_id = serializers.IntegerField()
    
    class Meta:
        model = Messages
        fields = ["user_id", "count"]


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


class EmotesTopSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    emote = serializers.CharField()
    
    class Meta:
        model = Messages
        fields = ["emote", "count"]