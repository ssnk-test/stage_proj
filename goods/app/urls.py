from django.urls import path

from . import views
from .views import StickerView

urlpatterns = [
    path('all/', StickerView.as_view()),
    ]