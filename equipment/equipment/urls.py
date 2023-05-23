"""
URL configuration for equipment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from equapi.views import EquipmentViewSet, TypeViewSet, UserViewSet

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


router = routers.DefaultRouter()
type_rout = routers.DefaultRouter()
user_rout = routers.DefaultRouter()
router.register('api/equipment', EquipmentViewSet, 'equipment_url')
router.register('api/equipment-type', TypeViewSet, 'type_url')
router.register('api/user/login', UserViewSet, 'user_urls')


urlpatterns = [
    path('admin/', admin.site.urls),

    # Router
    path('', include(router.urls)),

    
    # Swagger UI:
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

# Token
urlpatterns += [
    path('auth_token/', obtain_auth_token),
]
