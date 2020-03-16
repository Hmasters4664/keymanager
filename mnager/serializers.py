from user.models import User
from .models import Key
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('username', 'website', 'group', 'notes', 'password', 'slug')
        lookup_field = 'slug'