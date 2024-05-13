from django.contrib import admin
from django.urls import path, include
from testRandom.views import generate_test





from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('generate_test/',generate_test , name='generate_test'),
    path('', include(router.urls)),

    # Other URL patterns...
]



