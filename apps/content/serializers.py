from rest_framework import serializers
from .models import Category, Content, View, Like, Comment
from apps.chanel.serializers import GetChanelDataSerializers 



class ContentSerializers(serializers.ModelSerializer):
     views = serializers.SerializerMethodField()
     chanel_name = serializers.SerializerMethodField()
     likes_count = serializers.SerializerMethodField()

     class Meta:
          model = Content
          fields = ['id', 'title', 'description', 'photo', 'video', 'created_at', 
                    'views', 'category', 'author', 'chanel_name', 'likes_count']

     
     def get_views(self, obj):
          return obj.views.count()

     
     def get_chanel_name(self, obj):
          return GetChanelDataSerializers(instance=obj.author, context={'request': self.context.get('request')}).data


     def get_likes_count(self, obj):
          user = self.context.get('request').user.id
          like = Like.objects.filter(user=user, dislike=False)
          dislike = Like.objects.filter(user=user, dislike=True)
          is_liked = like.exists()
          is_disliked = dislike.exists()

          data = {
               'is_liked': is_liked,
               'is_disliked': is_disliked,
               'likes': obj.content_likes.filter(dislike=False).count(),
               'dislikes': obj.content_likes.filter(dislike=True).count()
          }

          return data



class UpdateContentSerializers(serializers.ModelSerializer):
     class Meta:
          model = Content
          fields = ['title', 'description', 'photo']



class CommentToContenSerializers(serializers.ModelSerializer):
     user = serializers.HiddenField(default=serializers.CurrentUserDefault())

     class Meta:
          model = Comment
          fields = ['id', 'user', 'content', 'comment']

     
     def create(self, validated_data):
          user = self.context.get('user')
          validated_data['user'] = user
          return super().create(validated_data)
     
     def to_representation(self, instance):
          data = super().to_representation(instance)
          data['user'] = instance.user.username

          return data



class UpdateCommentToContentSerializers(serializers.ModelSerializer):
     class Meta:
          model = Comment
          fields = ['comment']

     def update(self, instance, validated_data):
          instance.comment = validated_data.get('comment', instance.comment)
          instance.save()
          return instance



