from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'uId', 'first_name', 'last_name', 'email', 'phone', 'initials', 'color', 'status', 'last_login']