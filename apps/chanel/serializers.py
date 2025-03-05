from rest_framework import serializers
from .models import Chanel




class ChanelSerializer(serializers.ModelSerializer):

     subscriber_counts = serializers.SerializerMethodField()
     class Meta:
          model = Chanel
          fields = ['id', 'user', 'name', 'icon', 'banner', 'description', 'subscriber_counts']


     def get_subscriber_counts(self, obj):
          return obj.subscribers.all().count()


     def validate_name(self, value):

          if Chanel.objects.filter(name=value).exists():
               raise serializers.ValidationError("Bu nom bilan kanal mavjud")
               return value

          if len(value) < 5:
               raise serializers.ValidationError("Kanal nomi 5 ta belgidan kam bo'lishi mumkin emas")
               return value

          return value