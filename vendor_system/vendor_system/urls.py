
"""Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')"""

"""from vendorsite.views import vendorViewset
from django.urls import include,path
from rest_framework.routers import DefaultRouter

router= DefaultRouter()

router.register(r'vendors',vendorViewset,basename='vendor')
#urlpatterns=[*router.urls,]

urlpatterns= path('/vendors', vendorViewset.as_view({'post': 'create'}), name='create'),"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('vendorsite.urls')),
    path('admin/', admin.site.urls),
]