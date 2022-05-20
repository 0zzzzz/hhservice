from django.contrib.auth import authenticate
from rest_framework import serializers
from authapp.models import HhUser


class HhUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = HhUser
        fields = '__all__'

    def create(self, validated_data):
        return HhUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.password = validated_data.get('password', instance.password)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance

