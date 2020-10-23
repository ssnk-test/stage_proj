from django.db import models

# Create your models here.

class Tag(models.Model):
    text = models.CharField(max_length=20)


class Ad(models.Model):
    user_uuid = models.TextField(max_length=255)
    head = models.CharField(max_length=50)
    body = models.TextField(max_length=255)
    tag = models.ForeignKey(
        Tag, related_name="tags", on_delete=models.CASCADE, default=0
    )
    price = models.PositiveIntegerField()
    count_view = models.PositiveIntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to="pic/", null=True, blank=True)
