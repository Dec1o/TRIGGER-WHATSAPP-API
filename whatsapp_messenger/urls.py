from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WhatsAppSessionViewSet, MessageDispatchViewSet

router = DefaultRouter()
router.register(r'sessions', WhatsAppSessionViewSet)
router.register(r'messages', MessageDispatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]