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

