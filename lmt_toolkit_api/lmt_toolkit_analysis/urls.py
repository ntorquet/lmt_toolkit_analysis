'''
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('api/analyse', AnalyseLMTFile, basename="analyse")
router.register('api/reliability', ReliabilityLMTFile, basename="reliability")
router.register('api/files', FileViewSet, basename='files')
router.register('api/versions', VersionViewSet, basename='versions')
router.register('api/presets', PresetViewSet, basename='presets')
router.register('api/eventDocumentation', EventDocumentationViewSet, basename='eventDocumentation')

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('analyse_reliability/', views.analyse_reliability.as_view(), name="analyse_reliability"),
    path(r'api/read_file/', ReadFileAPIView.as_view(), name="read_file"),
    path(r'api/checkReliability/', CheckReliabilityAPIView.as_view(), name="checkReliability"),
    path(r'api/qualityControl/', QualityControlAPIView.as_view(), name="qualityControl"),
    path(r'api/rebuild/', RebuildSqliteAPIView.as_view(), name="rebuild"),
    path(r'api/rebuildNight/', RebuildNightEventAPIView.as_view(), name="rebuildNight"),
    path(r'api/saveAnimalInfo/', SaveAnimalInfoAPIView.as_view(), name="saveAnimalInfo"),
    path(r'api/extractAnalysis/', ExtractAnalysisAPIView.as_view(), name="extractAnalysis"),
    path(r'api/distancePerTimeBin/', DistancePerTimeBinAPIView.as_view(), name="distancePerTimeBin"),
    path(r'api/revokeTask/', StopCeleryTask.as_view(), name="revokeTask"),
    path(r'api/logInfo/', LogInfoAPIView.as_view(), name="logInfo"),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('djoser.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/', include('djoser.urls.authtoken')),
    re_path(r'^celery-progress/', include('celery_progress.urls')),
    # to download files:
    re_path(r'^media/uploaded/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
