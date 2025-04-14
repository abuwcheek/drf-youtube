from itertools import count
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import (CreateAPIView, UpdateAPIView,
                                   DestroyAPIView, RetrieveAPIView, 
                                   ListAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import  Category, CommentLike, CommentReply, Content, PlayList, View, Like, Comment
from .serializers import ( CategoryListSerializers, CategoryRetrieveSerializers, 
                         ContentCommentListSerializers, ContentSerializers, CreatePlayListSerializers, 
                         UpdateCommentReplyToContentSerializers,UpdateContentSerializers, 
                         CommentToContenSerializers, UpdateCommentToContentSerializers, 
                         CommentReplyToContentSerializers, CommentListToContentSerializers, 
                         RetrievePlayListSerializers, CategorySerializers,)
from .paginations import MyPageNumberPagination
from .permissions import IsHasChanel, IsOwner, IsAuthor
from apps.chanel.models import Chanel
from apps.chanel.serializers import GetChanelDataSerializers



class CreateContentAPIView(APIView):
     permission_classes = [IsAuthenticated, IsHasChanel]
     serializer_class = ContentSerializers

     def post(self, request):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid(raise_exception=True)
          content = serializer.save()
          chanel = request.user.chanel
          content.author = chanel
          content.save()

          data = {
               'status': True,
               'message': "video qo'shdingiz",
               'data': self.serializer_class(instance=content, context={'request': request}).data
          }

          return Response(data=data)



class UpdateContentAPIView(UpdateAPIView):
     permission_classes = [IsAuthenticated, IsOwner]
     serializer_class = UpdateContentSerializers
     queryset = Content.objects.filter(is_active=True)

     def update(self, request, *args, **kwargs):
          database = super().update(request, *args, **kwargs)
          data = {
               'status': True,
               'message': 'videoni o`zgartirdingiz',
               'data': database.data
          }
          return Response(data=data)



class DeleteContentAPIView(DestroyAPIView):
     permission_classes = [IsAuthenticated, IsOwner]
     serializer_class = UpdateContentSerializers
     queryset = Content.objects.filter(is_active=True)

     def destroy(self, request, *args, **kwargs):
          super().destroy(request, *args, **kwargs)

          data = {
               'status': True,
               'message': "videoni o'chirib tashladingiz"
          }

          return Response(data=data)



class RetrieveContentAPIView(RetrieveAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = ContentSerializers
     queryset = Content.objects.all()

     def retrieve(self, request, *args, **kwargs):
          content = self.get_object()
          if request.user.is_authenticated:
               user = request.user
               View.objects.get_or_create(user=user, content=content)

          # To‘g‘ri kontekstni serializatorga uzating
          serializer = ContentSerializers(instance=content, context={'request': request})
          return Response(serializer.data)


class ListContentAPIView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = ContentSerializers
     queryset = Content.objects.filter(is_active=True)
     pagination_class = MyPageNumberPagination



class LikeToContentAPIView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          video_id = request.data.get("video")

          video = get_object_or_404(Content, id=video_id)
          like = Like.objects.filter(video_id=video.id, user=request.user).first()
          dislike = request.data.get('dislike') == 'true'
          if like:
               if like.dislike == dislike:
                    like.delete()
                    data = {
                         'status': True,
                         'message': "like o'chirildi"
                    }
               else:
                    like.dislike = dislike
                    like.save()
                    data = {
                         'status': True,
                         'message': "like o'zgartirildi"
                    }
          else:
               Like.objects.create(video_id=video.id, user=request.user, dislike=dislike)
               data = { 
                    'status': True,
                    "message": "like bosildi"
               }
     
          return Response(data=data)
     


class CommetToContentAPIView(CreateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = CommentToContenSerializers
     queryset = Comment.objects.all()

     def get_serializer_context(self):
          context = super().get_serializer_context()
          context['user'] = self.request.user
          return context 



class UpdateCommentToContentAPIView(UpdateAPIView):
     permission_classes = [IsAuthenticated, IsAuthor]
     serializer_class = UpdateCommentToContentSerializers
     queryset = Comment.objects.filter(is_active=True)


     def update(self, request, *args, **kwargs):
          instance = self.get_object()
          if instance.user != request.user:
               data = {
                    'status': False,
                    'message': "bu comment sizga tegishli emas"
               }
               return Response(data=data)
          
          super().update(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "comment o'zgartirildi"
          }
          return Response(data=data)



class DeleteCommentToContentAPIView(DestroyAPIView):
     permission_classes = [IsAuthenticated, IsAuthor]
     serializer_class = CommentToContenSerializers
     queryset = Comment.objects.filter(is_active=True)


     def destroy(self, request, *args, **kwargs):
          instance = self.get_object()
          if instance.user != request.user:
               data = {
                    'status': False,
                    'message': "bu comment sizga tegishli emas"
               }
               return Response(data=data)

          super().destroy(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "comment o'chirildi"
          }
          return Response(data=data)



class LikeCommentToContentAPIView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          comment = get_object_or_404(Comment, id=request.data['comment'])
          like = CommentLike.objects.filter(comment=comment, user=request.user).first()
          dislike = request.data.get('dislike') == 'true'
          if like:
               if like.dislike == dislike:
                    like.delete()
                    data = {
                         'status': True,
                         'message': "like o'chirildi"
                    }
               else:
                    like.dislike = dislike
                    like.save()
                    data = {
                         'status': True,
                         'message': "like o'zgartirildi"
                    }
          else:
               CommentLike.objects.create(comment=comment, user=request.user, dislike=dislike)
               data = {
                    'status': True,
                    'message': "like bosildi"
               }
          
          return Response(data=data)



class CommentReplyToContentAPIView(CreateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = CommentReplyToContentSerializers
     queryset = CommentReply.objects.all()



class UpdateCommentReplyToContentAPIView(UpdateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = UpdateCommentReplyToContentSerializers
     queryset = CommentReply.objects.filter(is_active=True)

     def update(self, request, *args, **kwargs):
          super().update(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "comment reply o'zgartirildi"
          }
          return Response(data=data)



class DestroyCommentReplyToContentAPIView(DestroyAPIView):
     permission_classes = [IsAuthenticated, IsAuthor]
     serializer_class = UpdateCommentReplyToContentSerializers
     queryset = CommentReply.objects.filter(is_active=True)


     def delete(self, request, *args, **kwargs):
          super().delete(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "comment replay o'chirib tashlandi"
          }
          return Response(data=data)



class CommentListToContentAPIView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = CommentListToContentSerializers
     queryset = Comment.objects.filter(is_active=True)

     def get_queryset(self):
          id = self.kwargs.get('pk')
          content = get_object_or_404(Comment, id=id)
          comments = content.content_comments.filter(is_active=True)
          return comments



class CreatePlayListAPIView(CreateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = CreatePlayListSerializers
     queryset = PlayList.objects.all()

     def create(self, request, *args, **kwargs):
          solo = super().create(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "playlist yaratildi",
               'data': solo.data
          }
          return Response(data=data)



class AddContentToPlayListAPIView(APIView):
     permission_classes = [IsAuthenticated, IsAuthor]  # Foydalanuvchi va muallifga ruxsat

     def post(self, request, pk):
          content = get_object_or_404(Content, id=request.data['content'])
          playlist = get_object_or_404(PlayList, id=pk)

          if request.user == playlist.user:
               if content in playlist.videos.all():
                    playlist.videos.remove(content)  
                    data = {
                    'status': False,
                    'message': "video playlistdan o'chirildi"
                    }
                    return Response(data=data)
               else:
                    playlist.videos.add(content) 
                    data = {
                    'status': True,
                    'message': "video playlistga qo'shildi"
                    }
               return Response(data=data)
          else:
               data = {
                    'status': False,
                    'message': "afsuski siz playlist muallifi emassiz"
               }
               return Response(data=data)



class PlayListListAPIView(ListAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = CreatePlayListSerializers
     queryset = PlayList.objects.filter(is_active=True) 

     def get_queryset(self):
          user = self.request.user
          return PlayList.objects.filter(user=user, is_active=True)



class PlayListRetrieveAPIView(RetrieveAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = RetrievePlayListSerializers


     def get_queryset(self):
          user = self.request.user
          return PlayList.objects.filter(user=user)




class DeleteContentToPlayListAPIView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request, pk):
          content = get_object_or_404(Content, id=request.data['content'])
          playlist = get_object_or_404(PlayList, id=pk)

          if request.user == playlist.user:
               playlist.videos.remove(content)
               data = {
                    'status': True,
                    'message': "video playlistdan o'chirildi"
               }
          else:
               data = {
                    'status': False,
                    'message': "afsuski siz playlist muallifi emassiz"
               }

          return Response(data=data)



class DeletePlayListAPIView(DestroyAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = CreatePlayListSerializers
     queryset = PlayList.objects.filter(is_active=True)

     def destroy(self, request, *args, **kwargs):
          user = self.request.user
          playlist = get_object_or_404(PlayList, id=kwargs['pk'])
          if playlist.user == request.user or user.is_staff:
               self.perform_destroy(playlist)
               data = {
                    'status': True,
                    'message': "playlist o'chirildi"
               }
               return Response(data=data)


          data = {
               'status': False,
               'message': "afsuski siz playlist muallifi emassiz"
          }
     
          
          return Response(data=data)



class ContentCommentListAPIView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = ContentCommentListSerializers
     queryset = Comment.objects.filter(is_active=True)

     def get_queryset(self):
          content_id = self.kwargs.get('pk')
          return Comment.objects.filter(content_id=content_id, is_active=True).order_by('-created_at')



class CategoryCreateAPIView(CreateAPIView):
     permission_classes = [IsAdminUser]
     serializer_class = CategorySerializers
     queryset = Category.objects.all()

     def create(self, request, *args, **kwargs):
          category_name = request.data.get('title')
          if Category.objects.filter(title=category_name).exists():
               data = {
                    'status': False,
                    'message': "bunday kategoriya mavjud"
               }
               return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

          serializer = self.get_serializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          data = {
               'status': True,
               'message': "kategoriya yaratildi",
               'data': serializer.data,
          }     
          return Response(data=data, status=status.HTTP_201_CREATED)



class CategoryUpdateAPIView(UpdateAPIView):
     permission_classes = [IsAdminUser]
     serializer_class = CategorySerializers
     queryset = Category.objects.filter(is_active=True)

     def update(self, request, *args, **kwargs):
          data = super().update(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "kategoriya o'zgartirildi",
               'data': data.data
          }
          return Response(data=data)



class DestroyCategoryAPIView(DestroyAPIView):
     permission_classes = [IsAdminUser]
     serializer_class = CategorySerializers
     queryset = Category.objects.filter(is_active=True)

     def destroy(self, request, *args, **kwargs):
          super().destroy(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "kategoriya o'chirildi"
          }
          return Response(data=data)



class CategoryListAPIView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = CategoryListSerializers
     queryset = Category.objects.filter(is_active=True)



class CategoryRetrieveAPIView(RetrieveAPIView):
     permission_classes = [AllowAny]
     serializer_class = CategoryRetrieveSerializers
     queryset = Category.objects.filter(is_active=True)
     pagination_class = MyPageNumberPagination



class SearchVideosAPIView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = ContentSerializers

     def get_queryset(self):
          search = self.kwargs.get('search')
          return Content.objects.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(category__title__icontains=search) | Q(is_active=True))



class OrderByTimeAPIView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = ContentSerializers
     queryset = Content.objects.filter(is_active=True).order_by('-created_at')



class OrderByViewsAPIView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = ContentSerializers
     queryset = Content.objects.filter(is_active=True).order_by('-views__count')




class OrderByLikeAPIView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = Content

     def get_queryset(self):
          return Content.objects.annotate(
               likes_count=Count('likes', filter=Q(likes__dislike=False))  # Faqat like larni hisoblash
          ).order_by('-likes_count')