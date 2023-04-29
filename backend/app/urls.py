
from django.urls import path,include
from . import views 

# URL PATTERN FOR THE FILE UPLOAD TEST
from rest_framework import routers
from .views import FileViewSet, TwoFileViewSet, add_question

router = routers.DefaultRouter()

# so the api endpoint myfile/file/ is going to handle the file upload
router.register(r'file-upload', FileViewSet, basename='file-upload')
router.register(r'two-file-upload',TwoFileViewSet,basename="two-file-upload")

# END OF LINE FOR  URL PATTERN FOR THE FILE UPLOAD TEST
urlpatterns = [
    path("api/database-connection/",views.model_request,name="database-connection"),
    path('api/', include(router.urls)),
    path("api/add-question/", add_question,name = "add-question" )
]



