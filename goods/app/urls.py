from django.urls import path

from . import views
from .views import StickerList, StickerDetail,TagList
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('items/', StickerList.as_view()),
    path('items/<int:pk>/', StickerDetail.as_view()),
    path('tags/', TagList.as_view()),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)