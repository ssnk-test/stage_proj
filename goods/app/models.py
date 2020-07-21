from django.db import models

# Create your models here.

class Tag(models.Model):
    text = models.CharField(max_length=20)


class Sticker(models.Model):
    head = models.CharField(max_length=50)
    body = models.TextField(max_length=255)
    tag = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    count_view = models.PositiveIntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to="pic/", null=True, blank=True)
