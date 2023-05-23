from rest_framework import serializers
from equapi.models import Equipment, TypeEquipment
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User 


class EquipmentSerializer(serializers.ModelSerializer):
    serial_num = serializers.CharField(validators=[
        UniqueValidator(
            queryset=Equipment.objects.all(),
            message='Equipment with this serial number already exists'
        )
    ])
    class Meta:
        model = Equipment
        fields = ('id', 'type_eq', 'serial_num', 'note')


class TypeEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEquipment
        fields = ('id', 'name', 'mask_sn')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'username', 'password')
