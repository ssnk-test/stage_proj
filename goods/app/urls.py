from django.urls import path
from django.conf.urls import url

from . import views
from .views import StickerList, StickerDetail,TagList
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(title="API",default_version="None",),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r"^swagger/$",schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",),
    path('items/', StickerList.as_view()),
    path('items/<int:pk>/', StickerDetail.as_view()),
    path('tags/', TagList.as_view()),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)