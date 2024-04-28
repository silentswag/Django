from django.urls import path
from . import views

urlpatterns = [
    path('vendor/', views.vendor, name='vendor'),
]