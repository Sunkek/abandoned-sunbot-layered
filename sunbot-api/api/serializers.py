from rest_framework import serializers

from .models import User, Messages

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        exclude = ["id"] # Useless primary key field
