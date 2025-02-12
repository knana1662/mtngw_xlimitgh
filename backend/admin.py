from datetime import datetime
from heapq import merge
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from pandas import DataFrame
from .models import TransactionsDB,auth_users,Load_Backup_DB,VouchersDB
from django.contrib.auth import admin as auth_admin, models as auth_models , decorators , apps as auth_apps
from django.urls import path
from .views import index

from django.contrib.admin.models import LogEntry
from django.contrib.sites import  models as site_models ,admin as site_admin

from django.contrib.flatpages import admin as flatpages_admin,models as flatpages_models
from django.utils.translation import gettext_lazy as _
from django.forms import model_to_dict
from django.http import HttpResponse
import pandas as pd

# Register your models here.



class TransactionsDBAdmin(admin.ModelAdmin):
    list_display = ["Full_Name","Phone_Number","Data_Bundle","Voucher_Code","mtnTransactionId","Payment_Status","Voucher_Code_Recieved","Date_Created","created_by"]
    readonly_fields = list(merge(["id"],list_display)) #*
    ordering=["Date_Created"]
    search_fields=['Full_Name',"Phone_Number","Voucher_Code","mtnTransactionId"]
    search_help_text=f"Search by either : {' or '.join(search_fields).replace('_',' ')}"
    sortable_by=ordering
    actions = ["Export_To_Excel"]
    list_filter = ("Payment_Status" , "Voucher_Code_Recieved" , "Date_Created" , "created_by")
    
    @admin.action(description="Export To Excel")
    def Export_To_Excel(self,requests,queryset:list):
        ...
        list_of_selected_data = [
            {

                "Full_Name":loop_queryset_dictionary["Full_Name"],
                "Phone_Number":loop_queryset_dictionary["Phone_Number"].replace("233","0"),
                "Data_Bundle":loop_queryset_dictionary["Data_Bundle"].split("__")[1],
                "Amount(¢)":loop_queryset_dictionary["Data_Bundle"].split("_")[0],
                "Voucher_Code":loop_queryset_dictionary["Voucher_Code"],
                "mtnTransactionId":loop_queryset_dictionary["mtnTransactionId"],
                "Payment_Status":loop_queryset_dictionary["Payment_Status"],
                "Voucher_Code_Recieved":loop_queryset_dictionary["Voucher_Code_Recieved"],
                "Date_Created":datetime.strftime(loop_queryset.Date_Created,"%Y-%m-%d %H:%M:%S"),
                "created_by":loop_queryset.created_by if loop_queryset.created_by != None else loop_queryset_dictionary["Phone_Number"],

            } 

            for idx,loop_queryset in enumerate(queryset)
            if (loop_queryset_dictionary := model_to_dict(loop_queryset))

        ]



        response = HttpResponse(headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="Kaneshi Transactions.csv"',
         })
        
        DataFrame(list_of_selected_data).to_csv(response)

        return response


    def save_form(self, request: auth_admin, form: auth_admin, change: auth_admin) -> auth_admin:
        form.instance.created_by = request.user
        return super().save_form(request, form, change)

class FlatPageAdmin(flatpages_admin.FlatPageAdmin):
    fieldsets = (
        ("Title",{'fields': ['title']}),
        ("Link / URL",{'fields': ['url']}),
        ("Add Template Name",{'fields': ['template_name']}),
        ("Add Message / Content",{'fields': ['content']}),
        ("Lists of sites",{'fields': ['sites']}),
        (_('Advanced options'),{
            'classes': ('collapse',),
            'fields': (
                    'enable_comments',
                    'registration_required',
            ),
        }
        ),
    )

class auth_UsersAdmin(auth_admin.UserAdmin):
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "is_active",
        "Phone_Number",
        "Date_Created",
        "created_by"
    ]

    fieldsets = (
        (
            None, {'fields': ('username', 'password')}
        ), 
        (
            'Personal info', {'fields': ('first_name', 'last_name', 'email',"Phone_Number")}
        ),
        (
            'Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
        (
            'Important dates', {'fields': ('last_login', 'date_joined')}
        )
    )

    list_filter = ("is_superuser" , "is_staff" , "is_active" , "Date_Created" , "created_by")


    def save_form(self, request: auth_admin, form: auth_admin, change: auth_admin) -> auth_admin:
        form.instance.created_by = request.user
        return super().save_form(request, form, change)

class LogEntry_Admin(admin.ModelAdmin):
    list_display = [
        "user",
        "content_type",
        "object_repr",
        "action_flag",
        "action_time"
    ]

    readonly_fields = list(merge(["object_id","change_message"],list_display))


def convert_csv_file(content):
    ...
    d = pd.read_csv(content)
    
    d.to_csv("output.csv", index=False)
    data = d.to_dict("records")
    for idx,loop_data in enumerate(data):
        Login = loop_data["Login"]
        Password = loop_data["Password"]
        Uptime_Limit = loop_data["Uptime Limit"]

        VouchersDB(
            username=Login,
            password=Password,
            uptime_limit=Uptime_Limit,
            claimed=False
        ).save()

    print("Data saved to output.csv")

class Load_Backup_DB_Admin(admin.ModelAdmin):
    list_display = ["description","File","Date_Created","created_by"]

    list_filter = ("Date_Created" , "created_by")


    def save_model(self, request, obj, form, change):
        ...

        convert_csv_file(content = request.FILES["File"].file)
        return super().save_model(request, obj, form, change)

    def save_form(self, request: auth_admin, form: auth_admin, change: auth_admin) -> auth_admin:
        form.instance.created_by = request.user
        return super().save_form(request, form, change)

class VoucherDBAdmin(admin.ModelAdmin):
    list_display = ["username","password","uptime_limit","claimed"]
    readonly_fields = list(merge(["id"],list_display)) #*
    ordering=["username"]
    search_fields=list_display
    search_help_text=f"Search by either : {' or '.join(search_fields).replace('_',' ')}"
    sortable_by=ordering
    actions = ["Export_To_Excel"]
    list_filter = ("username","password","uptime_limit","claimed")
    
    @admin.action(description="Export To Excel")
    def Export_To_Excel(self,requests,queryset:list):
        ...
        list_of_selected_data = [
            {

                "username":loop_queryset_dictionary["username"],
                "password":loop_queryset_dictionary["password"],
                "uptime_limit":loop_queryset_dictionary["uptime_limit"],
                "claimed":loop_queryset_dictionary["claimed"],

            } 

            for idx,loop_queryset in enumerate(queryset)
            if (loop_queryset_dictionary := model_to_dict(loop_queryset))

        ]



        response = HttpResponse(headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="Kaneshi Transactions.csv"',
         })
        
        DataFrame(list_of_selected_data).to_csv(response)

        return response


    def save_form(self, request: auth_admin, form: auth_admin, change: auth_admin) -> auth_admin:
        form.instance.created_by = request.user
        return super().save_form(request, form, change)



admin.site.register(Load_Backup_DB,Load_Backup_DB_Admin)
admin.site.register(auth_users,auth_UsersAdmin)
admin.site.register(LogEntry,LogEntry_Admin)
admin.site.register(TransactionsDB,TransactionsDBAdmin)
admin.site.register(VouchersDB,VoucherDBAdmin)
