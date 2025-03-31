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
     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
     is_followed = serializers.SerializerMethodField()
     followers_count = serializers.SerializerMethodField()

     class Meta:
          model = Chanel
          fields = ['id', 'user', 'name', 'icon', 'is_followed', 'followers_count']


     def get_is_followed(self, obj):
          request = self.context.get("request", None)  # request mavjudligini tekshiramiz
          if request is None or not hasattr(request, "user"):
               return False  # request yo‘q bo‘lsa, False qaytarish
          return request.user.is_authenticated and request.user in obj.subscribers.all()




     @staticmethod
     def get_followers_count(obj):
          return obj.subscribers.all().count()