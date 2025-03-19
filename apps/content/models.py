from django.db import models
from apps.accounts.models import CustomUser
from apps.base.models import BaseModel
from apps.chanel.models import Chanel



class Category(BaseModel):
     title = models.CharField(max_length=255)


     def __str__(self):
          return self.title



class Content(BaseModel):
     title = models.CharField(max_length=255)
     description = models.TextField(null=True, blank=True)
     photo = models.ImageField(upload_to='content_photo/')
     video = models.FileField(upload_to='content_video/' )
     category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='category_videos', null=True, blank=True)
     author = models.ForeignKey(Chanel, on_delete=models.CASCADE, related_name='author_videos', null=True, blank=True)


     def __str__(self):
          return self.title



class View(BaseModel):
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='views')
     content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='views')


     def __str__(self):
          return f"{self.user.username} - {self.content.title}"



class Like(BaseModel):
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_likes')
     video = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='content_likes')
     dislike = models.BooleanField(default=False)


     def __str__(self):
          return f"{self.user.username} - {self.video.title}"



class Comment(BaseModel):
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_comments')
     content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='content_comments')
     comment = models.TextField()


     def __str__(self):
          return f"{self.user.username} - {self.content.title}"



class CommentLike(BaseModel):
     user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='user_comment_likes', null=True, blank=True)
     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
     dislike = models.BooleanField(default=False)


     def __str__(self):
          return f'{self.user.username} - {self.comment.comment}'



class CommentReply(BaseModel):
     user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='comment_replys', null=True, blank=True)
     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_replys')
     reply = models.TextField()


     def __str__(self):
          return f'{self.user.username} - {self.comment.comment}'
     


class PlayList(BaseModel):
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_playlist')
     title = models.CharField(max_length=200)
     videos = models.ManyToManyField(Content, related_name='videos_playlists', blank=True)