from django.urls import path, include
from equapi.views import index


urlpatterns = [
    path('home/', index)
]