from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.api.views import UserProfileViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]