from django.urls import path
from .views import (CreateContentAPIView, UpdateContentAPIView, 
                    DeleteContentAPIView, RetrieveContentAPIView, 
                    ListContentAPIView, LikeToContentAPIView,
                    CommetToContentAPIView, UpdateCommentToContentAPIView,
                    DeleteCommentToContentAPIView, LikeCommentToContentAPIView,
                    CommentReplyToContentAPIView, UpdateCommentReplyToContentAPIView,
                    DestroyCommentReplyToContentAPIView, CommentListToContentAPIView)




urlpatterns = [
     path('create-content', CreateContentAPIView.as_view()),
     path('update-content/<int:pk>', UpdateContentAPIView.as_view()),
     path('delete-content/<int:pk>', DeleteContentAPIView.as_view()),
     path('retrieve-content/<int:pk>', RetrieveContentAPIView.as_view()),
     path('list-content', ListContentAPIView.as_view()),
     path('like-to-content', LikeToContentAPIView.as_view()),
     path('comment-to-content', CommetToContentAPIView.as_view()),
     path('update-comment-to-content/<int:pk>', UpdateCommentToContentAPIView.as_view()),
     path('delete-comment-to-content/<int:pk>', DeleteCommentToContentAPIView.as_view()),
     path('lke-comment', LikeCommentToContentAPIView.as_view()),
     path('comment-reply', CommentReplyToContentAPIView.as_view()),
     path('update-comment-reply/<int:pk>', UpdateCommentReplyToContentAPIView.as_view()),
     path('delete-comment-reply/<int:pk>', DestroyCommentReplyToContentAPIView.as_view()),
     path('content-comments/<int:pk>', CommentListToContentAPIView.as_view()),
]