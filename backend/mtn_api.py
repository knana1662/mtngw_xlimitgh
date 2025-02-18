from datetime import datetime, timedelta
import random
import string
from time import sleep
from requests import post,get
from uuid import uuid4
from os import getenv
from base64 import b64encode
from asgiref.sync import async_to_sync
from channels.exceptions import ChannelFull
from core.settings import channel_layer
from .connector import store_in_transactions_db
from threading import Thread
from django.forms import model_to_dict
from .sms import send_sms
from .mikrotik_api import create_and_get_user






def mtn_payment_gateway(self):
    ...

    API_USER = getenv("API_USER") # Get credentials for api user
    API_KEY = getenv("API_KEY") # Get credentials for api key
    PRIMARY_KEY = getenv("PRIMARY_KEY")# Get credentials for Primary key
    SECONDARY_KEY = getenv("SECONDARY_KEY")# Get credentials for Secondary key
    TARGET_ENV = getenv("TARGET_ENV") # Get target
    X_REFERENCE_ID = getenv("X_REFERENCE_ID") # Get target
    CALLBACKHOST = getenv("CALLBACKHOST") # Get callback

    AUTHORIZATION_KEY = f'Basic {b64encode(f"{API_USER}:{API_KEY}".encode("utf-8")).decode("utf-8")}'

    # HOST_URL = "sandbox.momodeveloper.mtn.com" #* TEST URL
    HOST_URL = "proxy.momoapi.mtn.com" #* PRODUCTION URL

    headers = {
        "Ocp-Apim-Subscription-Key":f"{PRIMARY_KEY}", #PRIMARY KEY is the same as "Ocp-Apim-Subscription-Key" and Subscription Key 
        "Authorization":AUTHORIZATION_KEY,
        "X-Target-Environment" : f"{TARGET_ENV}",
        "X-Reference-Id":f"{X_REFERENCE_ID}",
        "Content-Type": "application/json",
        "Cache-Control":"no-cache",
                
    }


    user_info = {
        "amount": f'{self.request.session["amount"]}',
        "currency": "GHS", # if sandbox use "EUR" else if production use "GHS"
        "externalId": f"{uuid4()}",# REFERENCE CODE
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": f'233{self.request.session["Phone_Number"].lstrip("0")}' # PHONE NUMBER
        },
        "payerMessage": "Payment",
        "payeeNote": "pay me"
    }

    def mtngw_xlimitgh_access_token():
        ...
        with post(f"https://{HOST_URL}/collection/token/",headers=headers) as create_token:
            ...

            if create_token.status_code == 200:
                ...
                print(f"{create_token.status_code=}")

                headers.update(
                    {
                        "Authorization": f'Bearer {create_token.json()["access_token"]}',
                    }
                )

                return headers

    def mtngw_xlimitgh_requestpayment(headers):
        ...

        if mtngw_xlimitgh_check_if_phone_number_is_active(headers) == True:

            headers.update(
                {
                    "X-Reference-Id":f"{uuid4()}"
                }
            )

            with post(f"https://{HOST_URL}/collection/v1_0/requesttopay",headers=headers,json= user_info) as make_payment:
                ...

                if make_payment.status_code == 202:
                    print(f"{make_payment.status_code=}\n")
                    Thread(target = mtngw_xlimitgh_verify_transactions_status,args=[headers],daemon=True,name="mtngw_xlimitgh_verify_transactions_status").start()

        else:
            print(f'{user_info["payer"]["partyId"]} is neither registered nor active')

    def mtngw_xlimitgh_get_balance(headers):
        ...

        with get(f"https://{HOST_URL}/collection/v1_0/account/balance",headers=headers) as get_balance:
            # print(f"{headers=}")
            ...
            if get_balance.status_code == 200:
                print(f"{get_balance.status_code=}\n")
                print(f"{get_balance.json()=}\n")

            else:
                print(f"{get_balance.reason=}")
                print(f"{get_balance.json()=}")

    def mtngw_xlimitgh_verify_transactions_status(headers):
        ...

        with get(f"https://{HOST_URL}/collection/v1_0/requesttopay/{headers['X-Reference-Id']}",headers=headers) as verify_transactions_status:
            ...
            if verify_transactions_status.status_code == 200:
                            
                print(f"{verify_transactions_status.status_code=}\n")

                status = verify_transactions_status.json()["status"]
                reason = verify_transactions_status.json().get("reason")

                if status.lower().startswith("success"):
                    print(f"{status=}\n{reason=}\n")

                    financialTransactionId = verify_transactions_status.json()["financialTransactionId"]

                    self.request.session.update(
                        {   "mtnTransactionId":financialTransactionId,
                            "status":"Payment Successful."
                        }
                    )

                    try:
                        async_to_sync(channel_layer)(
                            "transactions_status",
                            {
                                "type": "transactions_status",
                                "message": {
                                    "status":status,
                                    "details":"Payment is Successful"
                                },
                            }
                        )

                    except ChannelFull:
                        ...

                    print("transaction successful")

                    print(self.request.session["Full_Name"],self.request.session["Phone_Number"],self.request.session["user_data_bundle"],self.request.session["voucher_code"],self.request.session["mtnTransactionId"])
                    
                    get_created_user = create_and_get_user(
                        profile=self.request.session["amount"],
                        hotspot_username=''.join(random.choice(string.ascii_lowercase) for x in range(4)).join(random.choice(string.digits) for x in range(2)) , 
                        hotspot_password=''.join(random.choice(string.ascii_lowercase) for x in range(4)).join(random.choice(string.digits) for x in range(2)) 
                    )

                    voucher_code_username = get_created_user["hotspot_user"]
                    voucher_code_password = get_created_user["hotspot_password"]
                    voucher_code = f"{voucher_code_username} - {voucher_code_password}"
                    
                    print(get_created_user)
                    
                    if get_created_user:
                        ...
                        # send_sms(
                        #     self,
                        #     self.request.session["Phone_Number"],
                        #     f'Hotspot Username : {voucher_code_username}\nHotspot Password : {voucher_code_password}'
                        # )

                        send_sms(
                            self,
                            self.request.session["Phone_Number"],
                            f'You have successfully purchased {self.request.session["data"].replace("_(","  valid for ").replace(")","").replace("_"," ")} at GHc{self.request.session["amount"]}.\nHotspot Username : {voucher_code_username}\nHotspot Password : {voucher_code_password}\nTransaction ID : {self.request.session["mtnTransactionId"]}'
                        )

                        store_in_transactions_db_thread = Thread(target=store_in_transactions_db,args=(self.request.session["Full_Name"],self.request.session["Phone_Number"],self.request.session["user_data_bundle"],voucher_code,self.request.session["mtnTransactionId"],True,True))
                        store_in_transactions_db_thread.start() #*

                        self.request.session.update(
                            {
                                "status":"Voucher Code is Sent Successfully."
                            }
                        )

                        print(f"[SUCCESS] - {self.request.session['Phone_Number']} purchased {self.request.session['data']}")                                                     

                        mtngw_xlimitgh_get_balance(headers = headers)

                    else:
                        print("No voucher code left to be claimed!!")
                        
                elif status.lower().startswith("pending"):
                    print(f"{status=}\n{reason=}\n")

                    set_global_time = timedelta(seconds=datetime.now().timestamp()) + timedelta(seconds=5)

                    while 1:
                        try:
                            get_remaining_seconds = timedelta(seconds=set_global_time.total_seconds()) - timedelta(seconds=datetime.now().timestamp())

                            if int(get_remaining_seconds.total_seconds()) == 0:

                                try:
                                    async_to_sync(channel_layer)(
                                        "transactions_status",
                                        {
                                            "type": "transactions_status",
                                            "message": {
                                                "status":status,
                                                "details":"Processing Payment. \n Please Wait"
                                            },
                                        }
                                    )

                                except ChannelFull:
                                    ...

                                print("transaction processing")

                                mtngw_xlimitgh_verify_transactions_status(headers = headers)


                            else:
                                ...
                                sleep(1)
                        except RecursionError:
                            ...
                            mtngw_xlimitgh_verify_transactions_status(headers = headers)

                else:
                    print(f"{status=}\n{reason=}\n")

                    self.request.session.update(
                        {
                            "status":"Payment Failed.\nPlease Try Again. "
                        }
                    )

                    try:
                        async_to_sync(channel_layer)(
                            "transactions_status",
                            {
                                "type": "transactions_status",
                                "message": {
                                    "status":status,
                                    "details":"Payment is Unsuccessful. \nPlease Try Again"
                                },
                            }
                        )

                    except ChannelFull:
                        ...

                    print("transaction failed")

                headers.update(
                    {
                        "X-Reference-Id":X_REFERENCE_ID
                    }
                )

    def mtngw_xlimitgh_check_if_phone_number_is_active(headers):
        ...

        with get(f"https://{HOST_URL}/collection/v1_0/accountholder/msisdn/{user_info['payer']['partyId']}/active",headers=headers) as check_if_phone_number_is_active:
            ...

            if check_if_phone_number_is_active.status_code == 200:
                print(f"{check_if_phone_number_is_active.status_code=}\n")

                return check_if_phone_number_is_active.json()["result"]

    access_token = mtngw_xlimitgh_access_token()
    mtngw_xlimitgh_requestpayment(headers = access_token)
    mtngw_xlimitgh_get_balance(headers = access_token)

