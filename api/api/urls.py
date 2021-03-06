"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from main import views

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'step-config', views.StepConfigViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^columns/(?P<project_id>\d+)?', views.schema),
    url(r'^upload-file', views.upload),
    url(r'^download-file/(?P<filename>.+)/(?P<name>.+)/$',views.download),
    url(r'^output-fields/(?P<project_id>\d+)?', views.output_fields),
    url(r'^available-modules/(?P<step>[\w-]+)/(?P<project_id>\d+)?', views.available_modules),
    url(r'^run/', views.run),
    url(r'^preview-data/(?P<step>[\w-]+)/(?P<project_id>\d+)?', views.previewdata),
    url(r'^segmented-schema/(?P<project_id>\d+)?', views.segmentedschema),
    url(r'^global-schema/(?P<project_id>\d+)?', views.globalschema),
    url(r'^final-schema/(?P<project_id>\d+)?', views.finalschema),
    url(r'^indexing-data/(?P<project_id>\d+)?', views.indexingdata),
    url(r'^comparison-data/(?P<project_id>\d+)?', views.comparisondata),
    url(r'^matches-result/(?P<project_id>\d+)?', views.matchesresult),
    url(r'^fused-data/(?P<project_id>\d+)?', views.fuseddata),
    url(r'^get-script/(?P<project_id>\d+)?',views.get_script)
]
