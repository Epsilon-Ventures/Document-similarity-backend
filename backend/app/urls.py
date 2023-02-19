
from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path("api/database-connection/",views.model_request,name="database-connection"),
]
