from rest_framework import serializers
from .models import Category, CommentLike, CommentReply, Content, PlayList, View, Like, Comment
from apps.chanel.serializers import GetChanelDataSerializers 



class ContentSerializers(serializers.ModelSerializer):
     views = serializers.SerializerMethodField()
     chanel_name = serializers.SerializerMethodField()
     likes_count = serializers.SerializerMethodField()
     comment_list = serializers.SerializerMethodField()

     class Meta:
          model = Content
          fields = ['id', 'title', 'description', 'photo', 'video', 'created_at', 
                    'views', 'category', 'author', 'chanel_name', 'likes_count', 'comment_list']

     
     def get_views(self, obj):
          return obj.views.count()
     

     def get_comment_list(self, obj):
          comments = obj.content_comments.all()
          return CommentListToContentSerializers(instance=comments, many=True).data

     
     def get_chanel_name(self, obj):
          return GetChanelDataSerializers(instance=obj.author, context={'request': self.context.get('request')}).data


     def get_likes_count(self, obj):
          user = self.context.get('request').user

          if user.is_authenticated:
               like = Like.objects.filter(user=user, video=obj, dislike=False)
               dislike = Like.objects.filter(user=user, video=obj, dislike=True)

               is_liked = like.exists()
               is_disliked = dislike.exists()
          else:
               is_liked = False
               is_disliked = False

          data = {
               'is_liked': is_liked,
               'is_disliked': is_disliked,
               'likes': obj.content_likes.filter(dislike=False).count(),
               'dislikes': obj.content_likes.filter(dislike=True).count(),
          }
          return data



class ContentListSerializers(serializers.ModelSerializer):
     chanel_name = serializers.SerializerMethodField()
     views = serializers.SerializerMethodField()

     class Meta:
          model = Content
          fields = ['id', 'title', 'photo', 'video', 'category', 'author', 'chanel_name', 'views', 'created_at']



     def get_views(self, obj):
          return obj.views.count()


     def get_chanel_name(self, obj):
          return GetChanelDataSerializers(instance=obj.author, context={'request': self.context.get('request')}).data




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



class CommentReplyToContentSerializers(serializers.ModelSerializer):
     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
     class Meta:
          model = CommentReply
          fields = ['id', 'user', 'comment', 'reply']

     def to_representation(self, instance):
          data = super().to_representation(instance)
          data['user'] = instance.user.username
          return data



class UpdateCommentReplyToContentSerializers(serializers.ModelSerializer):
     class Meta:
          model = CommentReply
          fields = ['reply']

     def update(self, instance, validated_data):
          instance.reply = validated_data.get('reply', instance.reply)
          instance.save()
          return instance



class CommentListToContentSerializers(serializers.ModelSerializer):
     likes_count = serializers.SerializerMethodField()
     comment_replies = serializers.SerializerMethodField()

     class Meta:
          model = Comment
          fields = ['id', 'comment', 'user', 'likes_count', 'comment_replies']

     def get_likes_count(self, obj):
          # Request kontekstdan olish va userni tekshirish
          request = self.context.get('request')
          if request and hasattr(request, 'user'):
               user = request.user
               like = CommentLike.objects.filter(user=user, comment=obj, dislike=False)
               dislike = CommentLike.objects.filter(user=user, comment=obj, dislike=True)
               is_liked = like.exists()
               is_disliked = dislike.exists()

               return {
                    'is_liked': is_liked,
                    'is_disliked': is_disliked,
                    'comment_likes': obj.comment_likes.filter(dislike=False).count(),
                    'comment_dislikes': obj.comment_likes.filter(dislike=True).count(),
               }
          return {
               'is_liked': False,
               'is_disliked': False,
               'comment_likes': 0,
               'comment_dislikes': 0,
          }

     def get_comment_replies(self, obj):
          comments = obj.replies.all()
          return CommentReplyToContentSerializers(instance=comments, many=True, context=self.context).data



class CommentLikeSerializer(serializers.ModelSerializer):
     class Meta:
          model = CommentLike
          fields = ['id', 'comment', 'user', 'dislike']


class CreatePlayListSerializers(serializers.ModelSerializer):
     videos_count = serializers.SerializerMethodField()
     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
     class Meta:
          model = PlayList
          fields = ['id', 'user', 'title', 'videos_count']

     
     def get_videos_count(self, obj):
          return obj.videos.count()



class RetrievePlayListSerializers(serializers.ModelSerializer):
     videos = serializers.SerializerMethodField()
     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
     class Meta:
          model = PlayList
          fields = ['id', 'title', 'videos',  'user']


     @staticmethod
     def get_videos(obj):
          vds = obj.videos
          return ContentSerializers(instance=vds, many=True).data



class ContentCommentListSerializers(serializers.ModelSerializer):
     likes_count = serializers.SerializerMethodField()
     comment_replies = serializers.SerializerMethodField()
     class Meta:
          model = Comment
          fields = ['id', 'comment', 'user', 'likes_count', 'comment_replies']

     def get_likes_count(self, obj):
          user = self.context.get('request').user
          like = CommentLike.objects.filter(user=user, comment=obj, dislike=False)
          dislike = CommentLike.objects.filter(user=user, comment=obj, dislike=True)
          is_liked = like.exists()
          is_disliked = dislike.exists()
          data = {
               'is_liked': is_liked,
               'is_disliked': is_disliked,
               'likes': obj.comment_likes.filter(dislike=False).count(),
               'dislikes': obj.comment_likes.filter(dislike=True).count(),
          }
          return data


     def get_comment_replies(self, obj):
          comments = obj.comment_replies.all()
          return CommentReplyToContentSerializers(instance=comments, many=True).data




class CategorySerializers(serializers.ModelSerializer):
     class Meta:
          model = Category
          fields = ['id', 'title']



class CategoryListSerializers(serializers.ModelSerializer):
     contents = serializers.SerializerMethodField()
     class Meta:
          model = Category
          fields = ['id', 'title', 'contents']


     @staticmethod
     def get_contents(obj):
          return obj.category_videos.all().filter(is_active=True).count()



class CategoryRetrieveSerializers(serializers.ModelSerializer):
     contents = serializers.SerializerMethodField()
     class Meta:
          model = Category
          fields = ['id', 'title', 'contents']


     @staticmethod
     def get_contents(obj):
          contents = obj.category_videos.all().filter(is_active=True).order_by('-created_at')
          return ContentSerializers(instance=contents, many=True).data



class SearchContentSerializers(serializers.ModelSerializer):
     chanel_name = serializers.SerializerMethodField()
     views = serializers.SerializerMethodField()

     class Meta:
          model = Content
          fields = ['id', 'title', 'photo', 'video', 'category', 'author', 'chanel_name', 'views', 'created_at']


     def get_views(self, obj):
          return obj.views.count()


     def get_chanel_name(self, obj):
          return GetChanelDataSerializers(instance=obj.author, context={'request': self.context.get('request')}).data
