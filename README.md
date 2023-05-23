# Equipment Api

### An entity that allows you to work with equipment
---

## Requirements
- Django(4.2.1)
- Python(3.10.3)
- djangorestframework
- drf-spectacular(0.26.2)
---
## Installation
First of all we need to install **dependencies** using pip 

- Install Python

`pip install python==3.10.3`

- Install Django

`pip install django==4.2.1`

- Install djangorestframework

`pip install djangorestframework`

- Install drf-spectacular(0.26.2)

`pip install drf-spectacular==0.26.2`

---

Connect to your base(mysql) `DATABASES`
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'base_name',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---
Add to your `INSTALLED_APPS`

```
INSTALLED_APPS = [
    ...
    # MyApp     
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    ...
]
```

Add settings for `REST_FRAMEWORK` to your project `settings.py`
```
REST_FRAMEWORK = {
    # Token Auth
    'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    ],

    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,

    # Permission
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),

    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

```

`SPECTACULAR_SETTINGS` 

```
SPECTACULAR_SETTINGS = {
    'TITLE': 'Equipment API',
    'DESCRIPTION': 'Equipment system Api',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}
```
---
Your urls should look like this
```
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
```
---
`signals.py` to create tokens

```
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```
## Examples
---
### Create a new user 

```
curl -X POST http://127.0.0.1:8000/api/user/login/  \ 
    -d '{
    "username": "test_user",
    "password": "string"
    }'
```
#### Response 
```
{
  "token": "aa6a76726e93fc1c039ef38a",
  "username": "test_user",
}
```

---
### Get a token
```
curl -X 'POST' 'http://localhost:8000/auth_token' \
    -d '{
    "username": "test_user",
    "password": "string"
    }'
```

#### Response 
```
{
  "token": "aa6a76726e93fc1c039ef38a"
}
```
---

### Create a equipment object. You can also use list of object

```
curl -X 'POST' \
  'http://localhost:8000/api/equipment/' \
  -H 'Authorization: Token 60a203bc25cdae3cb6e69285b79bb4ab0cbedcbd' \
  -d '{
      "type_eq": 2,
      "serial_num": "98XJO8-Zjo",
      "note": "Some note"
    }'
```

#### Response

```
[
  {
    "type_eq": 2,
    "serial_num": "98XJO8-Zjo",
    "note": "Some note"
  }
]
```
---

### Get a list of equipment object

```
curl -X 'GET' \
  'http://localhost:8000/api/equipment/' \
  -H 'Authorization: Token 60a203bc25cdae3cb6e69285b79bb4ab0cbedcbd'
```

#### Response

```
{
  "count": 23,
  "next": "http://localhost:8000/api/equipment/?limit=5&offset=5",
  "previous": null,
  "results": [
    {
      "id": 1,
      "type_eq": 2,
      "serial_num": "55IMO8-Zjo",
      "note": "string"
    },
    {
      "id": 2,
      "type_eq": 2,
      "serial_num": "92XJO8-Zjo",
      "note": "Some note"
    }
  ]
}
```

#### Also you can use `.../equipment/{id}/`

---

### Get a list of type equipment

```
curl -X 'GET' \
  'http://localhost:8000/api/equipment-type/' \
  -H 'Authorization: Token 60a203bc25cdae3cb6e69285b79bb4ab0cbedcbd'
```

#### Response

```
{
  "count": 7,
  "next": "http://localhost:8000/api/equipment-type/?limit=5&offset=5",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "TP-Link TL-WR74",
      "mask_sn": "XXAAAAAXAA"
    },
    {
      "id": 2,
      "name": "D-Link DIR-300",
      "mask_sn": "NXXAAXZXaa"
    },
    {
      "id": 3,
      "name": "D-Link DIR-300 E",
      "mask_sn": "NAAAAXZXXX"
    }
  ]
}
```

#### Also you can use `.../equipment-type/{id}/`
---

### Delete equipment object

```
curl -X 'DELETE' \
  'http://localhost:8000/api/equipment/{id}/' \
  -H 'Authorization: Token 60a203bc25cdae3cb6e69285b79bb4ab0cbedcbd' \
```

---

### Put equipment object

```
curl -X 'PUT' \
  'http://localhost:8000/api/equipment/{id}/' \
  -H 'Authorization: Token 60a203bc25cdae3cb6e69285b79bb4ab0cbedcbd' \

  -d '{
  "type_eq": 2,
  "serial_num": "98BJO8-Zjo",
  "note": "string"
}'
```

#### Response 

```
[
  {
    "type_eq": 2,
    "serial_num": "98BJO8-Zjo",
    "note": "string"
  }
]
```
