from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.base.models import BaseModel



class CustomUser(AbstractUser):

     GENDER_CHOICES = (
          ('JINS', 'Jins'),
          ('AYOL', 'Ayol'),
          ('ERKAK', 'Erkak'),
     )
     id = models.AutoField(primary_key=True)  # ID maydonini qo‘shish
     birth_date = models.DateField(null=True, blank=True)
     email = models.EmailField(unique=True)
     phono_numara = models.CharField(max_length=15, null=True, blank=True)
     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='JINS')


     def __str__(self):
          return f'{self.first_name} {self.last_name} >>> {self.email}'


