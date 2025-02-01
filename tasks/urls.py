from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from .models import Task
from .views import task_update_and_detail
urlpatterns = [
    path('task/', task_update_and_detail)
]

