from django.contrib import admin
from django.urls import path
from testRandom.views import generate_test


urlpatterns = [
    path('generate_test/',generate_test , name='generate_test'),
    # Other URL patterns...
]