
from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name = 'home'),
    path('api/', views.getData, name = "get-data"),
    path('api/response/', views.getModelResponse, name = "model-response"),
    path("api/second-model/",views.getSecondModel, name = "second-model"),
    path("api/database-connection/",views.database_connection,name="database-connection")
]
