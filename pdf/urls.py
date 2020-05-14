from django.urls import path
from . import views

app_name = "pdf"

urlpatterns = [
    path('', views.some_view, name='some_view'),
]