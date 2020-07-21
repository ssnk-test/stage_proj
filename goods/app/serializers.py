from rest_framework import serializers
from .models import Sticker, Tag


class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"