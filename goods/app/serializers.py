from rest_framework import serializers
from .models import Sticker

class StickerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    text = serializers.CharField()

    def create(self, validated_data):
        return Sticker.objects.create(**validated_data)
