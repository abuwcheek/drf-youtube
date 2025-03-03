from rest_framework import serializers
from .models import CustomUser




class CustomRegisterUserSerializer(serializers.ModelSerializer):
     class Meta:
          model = CustomUser
          fields = [ 'id', 'username', 'first_name', 'last_name', 'email', 'phono_numara', 'birth_date', 'gender', 'password']
          extra_kwargs = {'password': {'write_only': True}}


     def create(self, validated_data):
          user = CustomUser.objects.create_user(**validated_data)
          return user




class CustomUpdateUserSerializer(serializers.ModelSerializer):
     class Meta:
          model = CustomUser
          fields = ['first_name', 'last_name', 'email', 'phono_numara']
          extra_kwargs = {'email': {'read_only': True}}  # Email o‘zgarmasligi uchun



class CustomRetrieveUserSerializer(serializers.ModelSerializer):
     class Meta:
          model = CustomUser
          fields = [ 'id', 'username', 'first_name', 'last_name', 'email', 'phono_numara', 'birth_date', 'gender']