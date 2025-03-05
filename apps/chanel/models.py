from django.db import models

from apps.accounts.models import CustomUser
from apps.base.models import BaseModel



class Chanel(BaseModel):
     name = models.CharField(max_length=255)
     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='chanel', null=True, blank=True)
     icon = models.ImageField(upload_to='chanel_icon/', null=True, blank=True)
     banner = models.ImageField(upload_to='chanel_banner/', null=True, blank=True)
     description = models.TextField(null=True, blank=True)
     subscribers = models.ManyToManyField(CustomUser, related_name='chanel_subscribed', blank=True)


     def __str__(self):
          return self.name