from django.db import models

class xiechengItem(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    hot = models.CharField(max_length=100)
    day = models.DateField(max_length=100)
    url = models.CharField(max_length=100)

    class Meta:
        db_table = 'parkList'

class User(models.Model):
    uname = models.CharField(max_length=100, unique=True)
    upwd = models.CharField(max_length=100)
    utoken = models.CharField(max_length=100, default=None, null=True, blank=True)

    class Meta:
        db_table = 'user'

class Video(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=254,null=True)
    author = models.CharField(max_length=100)
    format = models.CharField(max_length=100)
    heat = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
