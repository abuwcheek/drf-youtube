from django.urls import path
from .views import (CategoryCreateAPIView, CategoryListAPIView, CategoryRetrieveAPIView, 
                    CategoryUpdateAPIView, CreateContentAPIView, DestroyCategoryAPIView, 
                    OrderByLikeAPIView, OrderByTimeAPIView, OrderByViewsAPIView, 
                    SearchVideosAPIView, UpdateContentAPIView, 
                    DeleteContentAPIView, RetrieveContentAPIView, 
                    ListContentAPIView, LikeToContentAPIView,
                    CommetToContentAPIView, UpdateCommentToContentAPIView,
                    DeleteCommentToContentAPIView, LikeCommentToContentAPIView,
                    CommentReplyToContentAPIView, UpdateCommentReplyToContentAPIView,
                    DestroyCommentReplyToContentAPIView, CommentListToContentAPIView,
                    CreatePlayListAPIView,AddContentToPlayListAPIView,
                    DeleteContentToPlayListAPIView,PlayListListAPIView,
                    PlayListRetrieveAPIView, DeletePlayListAPIView,
                    )



# content
urlpatterns = [
     path('create-content', CreateContentAPIView.as_view()),
     path('update-content/<int:pk>', UpdateContentAPIView.as_view()),
     path('delete-content/<int:pk>', DeleteContentAPIView.as_view()),
     path('retrieve-content/<int:pk>', RetrieveContentAPIView.as_view()),
     path('list-content', ListContentAPIView.as_view()),
]



# like and comment content
urlpatterns += [
     path('like-to-content', LikeToContentAPIView.as_view()),
     path('comment-to-content', CommetToContentAPIView.as_view()),
     path('update-comment-to-content/<int:pk>', UpdateCommentToContentAPIView.as_view()),
     path('delete-comment-to-content/<int:pk>', DeleteCommentToContentAPIView.as_view()),
     path('comments-list/<int:content_id>', CommentListToContentAPIView.as_view()),
     
]


# like and comment comment
urlpatterns += [
     path('like-comment', LikeCommentToContentAPIView.as_view()),
     path('comment-reply', CommentReplyToContentAPIView.as_view()),
     path('update-comment-reply/<int:pk>', UpdateCommentReplyToContentAPIView.as_view()),
     path('delete-comment-reply/<int:pk>', DestroyCommentReplyToContentAPIView.as_view()),
     path('content-comments/<int:pk>', CommentListToContentAPIView.as_view()),
]



# playlist
urlpatterns += [
     path('create-playlist', CreatePlayListAPIView.as_view()),
     path('add-content-to-playlist/<int:pk>', AddContentToPlayListAPIView.as_view()),
     path('delete-content-to-playlist/<int:pk>', DeleteContentToPlayListAPIView.as_view()),
     path('list-playlist', PlayListListAPIView.as_view()),
     path('retrieve-playlist/<int:pk>', PlayListRetrieveAPIView.as_view()),
     path('delete-playlist/<int:pk>', DeletePlayListAPIView.as_view()),
]



# category
urlpatterns += [
     path('category/create', CategoryCreateAPIView.as_view()),
     path('category/update/<int:pk>', CategoryUpdateAPIView.as_view()),
     path('destroy/category/<int:pk>', DestroyCategoryAPIView.as_view()),
     path('category/list', CategoryListAPIView.as_view()),
     path('category/retrieve/<int:pk>', CategoryRetrieveAPIView.as_view()),
]


# search, order
urlpatterns += [
     path('search-content/<str:search>', SearchVideosAPIView.as_view()),
     path('order-by-time', OrderByTimeAPIView.as_view()),
     path('order-by-views', OrderByViewsAPIView.as_view()),
     path('order-by-likes', OrderByLikeAPIView.as_view()),
]