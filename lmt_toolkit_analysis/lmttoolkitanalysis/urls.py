from django.conf import settings
from django.urls import include, path
from django.contrib.auth.models import User
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static


from . import views
from .views import *

router = DefaultRouter()
router.register('analyse_reliability', ReadFileViewSet, basename="analyse_reliability")

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('analyse_reliability/', views.analyse_reliability.as_view(), name="analyse_reliability"),
    path(r'read_file/', views.ReadFileAPIView.as_view(), name="read_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)