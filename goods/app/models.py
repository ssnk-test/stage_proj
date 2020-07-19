from django.db import models

# Create your models here.


class Sticker(models.Model):
    id = models.AutoField(primary_key=True)
    head = models.CharField(max_length=255)
    body = models.TextField()
    tag = models.CharField(max_length=20)
    price = models.CharField(max_length=20)

