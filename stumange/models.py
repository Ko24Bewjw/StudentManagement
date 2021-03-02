from django.db import models

# Create your models here.


class User1(models.Model):

  username=models.CharField(max_length=40,unique=True)
  pword=models.CharField(max_length=20)
