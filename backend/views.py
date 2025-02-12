from  pandas import ExcelWriter,DataFrame,read_excel 
from django.contrib import messages
    

from django.http import HttpResponse
from django.views.generic import TemplateView,FormView


from .connector import ENV_FILE,CAMBIUM_URL
from typing import Any, Dict
from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpRequest, HttpResponse, FileResponse
from .forms import TransactionsForms
from .models import TransactionsDB, auth_users
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache #*
from django.utils.decorators import method_decorator #*
from requests import post,exceptions
from os import getenv
from datetime import datetime
import random
import string
from glob import iglob
from .sms import send_sms
from .mtn_api import mtn_payment_gateway
from django.contrib.admin.views.decorators import staff_member_required
from .cache import generate_cache
from django.db.transaction import atomic
from django.views.decorators import debug as debug_decorator , csrf as csrf_decorator
from pathlib import Path
from sys import path
from django.core.management import call_command
from django.core.management.commands import loaddata
from tempfile import TemporaryDirectory,gettempdir
from shutil import rmtree
from sqlite3 import Connection

from .personal_decorators import optimization_timer

from core import SUBFOLDER_OF_ROOT_LOG_FOLDER,timeout,DATABASES

# Create your views here.

DATETIME=f"{datetime.today()}"[:19]

ENV_FILE

CAMBIUM_USERNAME = getenv("CAMBIUM_USERNAME")
CAMBIUM_PASSWORD = getenv("CAMBIUM_PASSWORD")




cambium_cookies = dict(cookies = None)




class index:


    class paywithMTN(TemplateView,FormView):
        model = TransactionsDB
        form_class = TransactionsForms
        template_name = 'index.html'
        success_url="otp"

        def form_valid(self, form: Any) -> HttpResponse:

            form_valid = super().form_valid(form)
            
            valid_data = form.cleaned_data  

            Data_Bundle=valid_data["Data_Bundle"]
            amount,data=Data_Bundle.split("_GHS__")          

            self.request.session.update(
                {
                    "id":None,
                    "Full_Name":valid_data["Full_Name"],
                    "Phone_Number":valid_data["Phone_Number"],
                    "user_data_bundle":Data_Bundle,
                    "amount":amount,
                    "data":data,
                    "otp":''.join(random.choice(string.digits) for x in range(4)).join(random.choice(string.digits) for x in range(2)),
                    "created_at":f"{datetime.now()}"[11:19],
                    "mtnTransactionId":None,
                    "uniwallet":{"headers":None,"json":None},
                    "sms_dictionary":{"id":None,"balance":None},
                    "charts":{"generated":None,"total_data":None,"used_data":None},
                    "voucher_code":None,
                    "status":None, #*
                    "sms_status":{"otp":False,"voucher":False,"notify-admins-and-managers":False} #*
                }
            ) #*


            print(f'{self.request.session["Phone_Number"]} - {self.request.session["otp"]}')
            print(self.request.session.items())


            send_sms(
                self,
                self.request.session["Phone_Number"],
                f"Here's your onetime otp : {self.request.session['otp']}"
            ) #* Send otp to clients

            print("SMS is sent successfully")

            print(self.request.session["sms_status"])



            return form_valid

        @method_decorator(
                [
                    # optimization_timer,
                    # csrf_decorator.csrf_exempt, #*
                    debug_decorator.sensitive_variables(),
                    atomic,
                    # atomic(durable=True),
                    # clickjacking_decorator.xframe_options_exempt,
                    never_cache, #*
                ]
        ) #*
        def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
            return super().get(request, *args, **kwargs)

    class verify_otp(TemplateView):
            template_name="otp.html"

            def get_context_data(self, **kwargs):
                get_context_data = super().get_context_data(**kwargs)

                return get_context_data
            
            @method_decorator(
                    [
                        # optimization_timer,
                        # csrf_decorator.csrf_exempt, #*
                        debug_decorator.sensitive_variables(),
                        never_cache,
                        atomic,
                        # atomic(durable=True),
                        # clickjacking_decorator.xframe_options_exempt,
                    ]
            ) #*
            def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
                get =  super().get(request, *args, **kwargs)
                
                return get

            @method_decorator(
                    [
                        csrf_decorator.csrf_exempt, #*
                        debug_decorator.sensitive_post_parameters(),
                    ]
            )
            def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

                if self.request.session.get("otp") != None: 
                    ...
                    if int(self.request.POST["otp"]) == int(self.request.session["otp"]) :
                        ...
                        
                        print("OTP Successfully Verified !! ")
                        self.request.session.pop("otp") #After the otp is verified the key in the session called "otp" is cleared to prevent user from using the same otp again

                        if ( "GB".lower() in self.request.session["data"].lower() )  or ( "MB".lower() in self.request.session["data"].lower() )  or ( "unlimited".lower() in self.request.session["data"].lower() ) : # Accepts data bundle that ends with GB

                            mtn_payment_gateway(self)

                        return render(self.request,"success.html",context={
                            "msg" : "<span id = 'status'> Please Wait ... </span> <br> <span id = 'details'></span> <br> Keep the page open",
                            }) #*

                    else:
                        ...   
                        print("Enter the correct voucher code")                                     
                        return render(self.request,"otp.html",context={
                            "msg" : "Enter the correct voucher code",
                            }) #*

                else:

                    return redirect("index")

    class callback_url(TemplateView):
        template_name = 'callback.html'


class errors:


    class BAD_REQUEST_400(TemplateView):
        ...
        template_name = "error.html"

        def get_context_data(self, **kwargs):
            get_context_data = super().get_context_data(**kwargs)
            get_context_data["status_code"] = "400"
            get_context_data["title"] = "BAD_REQUEST_400"
            get_context_data["details"] = "BAD REQUEST".capitalize()

            return get_context_data

    class PERMISSION_DENIED_403(TemplateView):
        ...
        template_name = "error.html"

        def get_context_data(self, **kwargs):
            get_context_data = super().get_context_data(**kwargs)
            get_context_data["status_code"] = "403"
            get_context_data["title"] = "PERMISSION_DENIED_403"
            get_context_data["details"] = "PERMISSION DENIED".capitalize()

            return get_context_data

    class PAGE_NOT_FOUND_404(TemplateView):
        ...
        template_name = "error.html"

        def get_context_data(self, **kwargs):
            get_context_data = super().get_context_data(**kwargs)
            get_context_data["status_code"] = "404"
            get_context_data["title"] = "PAGE_NOT_FOUND_404"
            get_context_data["details"] = "PAGE NOT FOUND".capitalize()

            return get_context_data

    class SERVER_ERROR_500(TemplateView):
        ...
        template_name = "error.html"

        def get_context_data(self, **kwargs):
            get_context_data = super().get_context_data(**kwargs)
            get_context_data["status_code"] = "500"
            get_context_data["title"] = "SERVER_ERROR_500"
            get_context_data["details"] = "SERVER ERROR".capitalize()

            return get_context_data

