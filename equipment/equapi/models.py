from django.db import models
from dataclasses import dataclass

from equapi.services.regex_check import check_mask_regex
from equapi.services.get_query import get_models
# Create your models here.

class TypeEquipment(models.Model):
    name = models.CharField(max_length=150)
    mask_sn = models.CharField(max_length=10)
    
    def __str__(self) -> str:
        return self.name


class Equipment(models.Model):
    type_eq = models.ForeignKey(TypeEquipment, on_delete=models.CASCADE, related_name='type_name')
    serial_num = models.CharField(max_length=10)
    note = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return f"Type - '{self.serial_num}'; Note - '{self.note}'"
    

    @classmethod
    def create_sn(cls, type_eq: int, serial_num: str, note: str ='No notes'):
        '''Create Equipment object'''
        model = get_models(TypeEquipment, pk=type_eq)[0]
        check_sn = cls.check_mask(serial_num, model.mask_sn)
        
        if type(check_sn) is bool:
            instance, created = Equipment.objects.get_or_create(
                type_eq_id=type_eq, 
                serial_num=serial_num,
                note=note
            )
            if not created:
                return {"messages": "Equipment with this serial number already exists"}
            return instance
            
        return check_sn

    @staticmethod
    def check_mask(serial_num: str, mask_sn: str) -> bool:
        '''Validation of the mask for compliance'''
        result = check_mask_regex(serial_num, mask_sn) 
        return result
