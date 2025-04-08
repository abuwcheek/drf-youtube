from django.urls import path

from rest_framework_simplejwt.views import (
     TokenObtainPairView,
     TokenRefreshView,
     )


urlpatterns = [
     # Token olish uchun
     path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),

     # Tokenni yangilash uchun
     path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]


from .views import CustomRegisterUserView, CustomUpdateUserView, CustomRetrieveUserView, CustomDeleteUserView, FollowChanelsListView, FollowUnfollowToChanelAPIView


urlpatterns += [
     path('register-user', CustomRegisterUserView.as_view(), name='register'),
     path('update-user', CustomUpdateUserView.as_view(), name='update'),
     path('retrieve-user', CustomRetrieveUserView.as_view(), name='retrieve'),
     path('delete-user', CustomDeleteUserView.as_view(), name='delete'),
]

urlpatterns += [
     path('follow-chanel', FollowUnfollowToChanelAPIView.as_view()),
     path('followed-chanels-user', FollowChanelsListView.as_view(), name='followed_chanels'),
]