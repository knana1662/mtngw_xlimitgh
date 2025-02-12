from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.forms import ValidationError, modelform_factory
from .models import TransactionsDB
from django.contrib.auth import forms as auth_forms,views as auth_views

TransactionsForms=modelform_factory(TransactionsDB,fields=["Full_Name","Phone_Number","Data_Bundle"],widgets={

    "Full_Name":forms.TextInput({"autocomplete":"on","placeholder":"Enter your name",'style':'width: 75%; height: 40px;margin-bottom:15px;border-radius: 10px; padding-left:10px; border:0.5px solid #ccc'}),
    "Phone_Number":forms.NumberInput({"autocomplete":"on","placeholder":"Enter your Momo number",'style': 'width: 75%; height: 40px;margin-bottom:15px;border-radius:10px;padding-left:10px;border:0.5px solid #ccc'}),
    "Data_Bundle":forms.RadioSelect(choices=TransactionsDB.bundleAllocations),

})

