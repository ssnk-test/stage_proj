from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import Ad, Tag
from .serializers import StickerSerializer, TagSerializer


class StickerList(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = StickerSerializer

    def post(self, request, *args, **kwargs):
        if "tag" in request.data:
            for item in request.data["tag"].split(","):
                Tag.objects.get_or_create(text=item)  # Небезопасный?

        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Ad.objects.all()

        params = self.request.data
        if "tags" in params:
            tags = params["tags"]
            queryset = queryset.filter(tag__in=tags)
        if "low_price" in params:
            queryset = queryset.filter(price__lte=params["low_price"])
        if "high_price" in params is not None:
            queryset = queryset.filter(price__gte=params["low_price"])

        return queryset


class StickerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = StickerSerializer
    def get(self, request, *args, **kwargs):
        print(request.query_params)
        if not request.query_params.get("service_view", None):
            sticker = get_object_or_404(self.queryset, pk=kwargs['pk'])
            sticker.count_view = F("count_view") + 1
            sticker.save()

        return self.retrieve(request, *args, **kwargs)


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
