
from django.urls import path,include
from . import views 

# URL PATTERN FOR THE FILE UPLOAD TEST
from rest_framework import routers
from .views import FileViewSet

router = routers.DefaultRouter()

# so the api endpoint myfile/file/ is going to handle the file upload
router.register(r'file-upload', FileViewSet, basename='file-upload')

# END OF LINE FOR  URL PATTERN FOR THE FILE UPLOAD TEST
urlpatterns = [
    path("api/database-connection/",views.model_request,name="database-connection"),
    path('api/', include(router.urls)),
]
