from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Sticker
from .serializers import StickerSerializer


class StickerView(APIView):
    def get(self, request):
        stickers = Sticker.objects.all()
        serializer = StickerSerializer(stickers, many=True)
        return Response({"articles": serializer.data})

    def post(self, request):
        sticker = request.data.get('sticker')
        # Create an article from the above data
        serializer = StickerSerializer(data=sticker)
        if serializer.is_valid(raise_exception=True):
            sticker_saved = serializer.save()
        return Response({"success": "created successfully"})