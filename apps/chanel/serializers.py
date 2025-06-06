from rest_framework import serializers
from .models import Chanel




class ChanelSerializer(serializers.ModelSerializer):

     subscribers_count = serializers.SerializerMethodField()
     class Meta:
          model = Chanel
          fields = ['id', 'user', 'name', 'icon', 'banner', 'description', 'subscribers_count']


     def get_subscribers_count(self, obj):
          return obj.subscribers.all().count()


     def validate_name(self, value):

          if Chanel.objects.filter(name=value).exists():
               raise serializers.ValidationError("Bu nom bilan kanal mavjud")
               return value

          if len(value) < 5:
               raise serializers.ValidationError("Kanal nomi 5 ta belgidan kam bo'lishi mumkin emas")
               return value

          return value



class GetChanelDataSerializers(serializers.ModelSerializer):
     username = serializers.SerializerMethodField()
     is_followed = serializers.SerializerMethodField()
     subscribers_count = serializers.SerializerMethodField()

     class Meta:
          model = Chanel
          fields = ['id', 'username', 'name', 'icon', 'is_followed', 'subscribers_count']

     def get_is_followed(self, obj):
          request = self.context.get('request')
          if request and request.user.is_authenticated:
               return obj.subscribers.filter(id=request.user.id).exists()
          return False

     def get_subscribers_count(self, obj):
          return obj.subscribers.count()

     def get_username(self, obj):
          return obj.user.username
