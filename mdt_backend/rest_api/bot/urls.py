from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BotInstanceViewSet


router = DefaultRouter()
router.register(r'bot-instance', BotInstanceViewSet, basename='bot_instance')

urlpatterns = [
    path('', include(router.urls)),
]