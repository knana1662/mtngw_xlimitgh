from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from django.db import models
import uuid
from .cache import generate_cache
from .custom_validators import validate_phone_number
from tempfile import gettempdir
from platform import system
from django.core.files.storage import FileSystemStorage

from core import test_bundle,get_all_data_allocations
from django.contrib.auth import models as auth_models

# Create your models here.



set_all_data_allocation = f'{test_bundle} {" ".join([set_all_data_allocation for idx,set_all_data_allocation in enumerate(get_all_data_allocations)])}'.strip()
print(set_all_data_allocation)

get_keys_and_values=[(x,x.split("_")[0]) for i,x in enumerate(set_all_data_allocation.split(" "))]

get_keys_and_values_dict = dict(get_keys_and_values = get_keys_and_values)

if get_keys_and_values_dict["get_keys_and_values"] != None:
    generate_cache(key="get_keys_and_values",condition="set",values_or_values=get_keys_and_values)
    # print(f'{generate_cache(key="get_keys_and_values",condition="get")=}')




class auth_users(auth_models.AbstractUser):
    Phone_Number = models.CharField(unique=False,max_length=10)
    
    Date_Created=models.DateTimeField(auto_created=True,auto_now=True)
    created_by = models.ForeignKey("auth_users", on_delete=models.SET_NULL, null=True,editable = False)


    def __str__(self):
        return self.username

class TransactionsDB(models.Model):
    id=models.UUIDField(unique=True,max_length=40,default=uuid.uuid4,primary_key=True)
    Full_Name=models.CharField(unique=False,max_length=40)
    Phone_Number=models.CharField(unique=False,max_length=10,validators=[validate_phone_number])
    bundleAllocations=models.TextChoices(get_all_data_allocations[0],set_all_data_allocation)
    Data_Bundle=models.CharField(max_length=30,choices=bundleAllocations.choices,default=get_all_data_allocations[0])
    Voucher_Code=models.CharField(max_length=15) #*
    mtnTransactionId=models.CharField(max_length=15,unique=True,null=True)
    Payment_Status=models.BooleanField(auto_created=True,default=False)
    Voucher_Code_Recieved=models.BooleanField(auto_created=True,default=False)
    Date_Created=models.DateTimeField(auto_created=True,auto_now=True)
        
    created_by = models.ForeignKey(auth_users, on_delete=models.SET_NULL, null=True,editable = False)

    def __str__(self) -> str:
        return f"{self.Full_Name} ({self.Phone_Number})"

class VouchersDB(models.Model):
    ...
    id=models.UUIDField(unique=True,max_length=40,default=uuid.uuid4,primary_key=True)
    username=models.CharField(unique=True,max_length=15)
    password=models.CharField(unique=True,max_length=15)
    uptime_limit=models.CharField(unique=False,max_length=150)
    claimed=models.BooleanField(unique=False)


    def __str__(self) -> str:
        return self.username


def select_file_storage_according_to_os_for_database_backup_files():
   if system().lower() == "linux":
      return FileSystemStorage(location=f'/{gettempdir()}/db',base_url='/db/')
   elif system().lower() == "windows":
      return FileSystemStorage(location=f'{gettempdir()}/db',base_url='/db/')


def validate_database_backup_file(value):
    if not f"{value}".endswith(".html") or value == None or value == "":
        print(f"{value=}")

        raise ValidationError(
            _('%(value)s Does not end with .html'),
            params={'value': value},
        ) 


class Load_Backup_DB(models.Model):
    ...
    description = models.CharField(max_length=21,help_text="Type(Description) of backup file")
    File = models.FileField(storage = select_file_storage_according_to_os_for_database_backup_files,validators=[validate_database_backup_file])
    Date_Created=models.DateTimeField(auto_created=True,auto_now=True)
    
    created_by = models.ForeignKey(auth_users, on_delete=models.SET_NULL, null=True,editable = False )


    def __str__(self):
        return self.description
