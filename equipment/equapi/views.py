from typing import List
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User 

from equapi.models import Equipment, TypeEquipment
from equapi.serializers import EquipmentSerializer, TypeEquipmentSerializer, UserSerializer
from equapi.services.get_query import get_models
from equapi.services.create_user_module import user_create

from rest_framework import viewsets, status, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token 
from rest_framework.filters import SearchFilter, OrderingFilter

from drf_spectacular.utils import extend_schema


class EquipmentViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('id', 'type_eq__name', 'serial_num', 'note')
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)


    @extend_schema(tags=['POST'], summary='Create Equipment object')
    def create(self, request, *args, **kwargs):
        # For single object
        if type(self.request.data) is not list:
            req_data = [self.request.data]
        else:
            req_data = self.request.data
        
        for data in req_data:
            response = self.perform_create(data=data)
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    @extend_schema(tags=['POST'], summary='Update Equipment object')
    def update(self, request, *args, **kwargs):
        response = self.perform_create(request.data)
        return Response(response, status=status.HTTP_201_CREATED)

    def perform_create(self, data) -> List[dict]:
        response = []
        serializer = self.get_serializer(data=data)

        try:  
            serializer.is_valid(raise_exception=True)

            type_eq = serializer.data.get("type_eq", None)
            serial_num = serializer.data.get("serial_num", None)
            note = serializer.data.get("note")

            result = Equipment.create_sn(type_eq, serial_num, note)

            if type(result) is dict:    
                response.append(result)
            else:
                response.append(serializer.data)

        except Exception as err:
            response.append(str(err))
        
        return response


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TypeEquipmentSerializer
    queryset = TypeEquipment.objects.all()
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('id', 'name', 'mask_sn')
    # permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.mixins.CreateModelMixin, 
                  viewsets.GenericViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(tags=['POST'], summary='Create user')
    def create(self, request, *args, **kwargs):
        '''Create User'''
        try:
            data = {}
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            username = serializer.data.get('username', None)
            password = serializer.data.get('password')
            user = user_create(username=username, password=password)

            token = Token.objects.get(user=user)

            data['token'] = token.key
            data['username'] = serializer.data['username']
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"message": str(e)},
                status.HTTP_400_BAD_REQUEST
            )


