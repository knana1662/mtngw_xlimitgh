import base64
import os
from pathlib import Path
from requests import get, post
from .connector import get_balance_of_either_uniwallet_or_jasmin,phone_number,send_sms_using_condition_phone_number_and_msg_content

BASE_DIR = Path(__file__).resolve().parent.parent

# path.append(f"{BASE_DIR}/core")
from core.settings import timeout



JASMIN_SMS_USERNAME=os.getenv("JASMIN_SMS_USERNAME")
JASMIN_SMS_PASSWORD=os.getenv("JASMIN_SMS_PASSWORD")
UNIWALLET_SMS_API=os.getenv("UNIWALLET_SMS_API")


credentials=f"{JASMIN_SMS_USERNAME}:{JASMIN_SMS_PASSWORD}"
auth_token=base64.b64encode(credentials.encode("utf-8")).decode("utf-8")


def check_sms_balance(self)->get_balance_of_either_uniwallet_or_jasmin:
    from .models import auth_users

    jasmine_headers={
        "Content-Type": "application/json",
        "Authorization":f"Basic {auth_token}"
    }
        
    uniwallet_headers={
        "Content-Type": "application/json"

    }

    uniwallet_json={
        "api_key": UNIWALLET_SMS_API,
        "merchant_id": 384,
        "async": False,
    }


    with get(url="http://66.228.38.61:8080/secure/balance",headers=jasmine_headers,timeout=timeout) as check_jasmine_sms_balance , get(url="http://52.89.222.13/tfsg/public/api/balance",json=uniwallet_json,headers=uniwallet_headers,timeout=timeout) as check_uniwallet_sms_balance:
        ...


        check_jasmine_sms_balance=check_jasmine_sms_balance.json()["data"]["sms_count"]      
        check_uniwallet_sms_balance=check_uniwallet_sms_balance.json()["balance"]



        if check_jasmine_sms_balance > check_uniwallet_sms_balance:
            if check_jasmine_sms_balance <= 100:
                print("Balance running out")
                for idx,loop_adminPhoneNumber in enumerate(auth_users.objects.all().values("username","Phone_Number")):
                    ...
                    send_sms( #*
                        self,
                        loop_adminPhoneNumber["Phone_Number"],
                        f"Balance running low .Please top-up .Remaining Balance : {check_jasmine_sms_balance}"
                    ) # Send notifications to admins and managers

            else:

                print(f"{check_jasmine_sms_balance=}")

                self.request.session.update(
                    {
                        "sms_dictionary":{
                            "id":"jasmine",
                            "balance":check_jasmine_sms_balance
                        }
                    }
                )

                return self.request.session


        else:
            if check_uniwallet_sms_balance <= 100:
                print("Balance running out")
                for idx,loop_adminPhoneNumber in enumerate(auth_users.objects.all().values("username","Phone_Number")):
                    ...
                    send_sms( #*
                        self,
                        loop_adminPhoneNumber["Phone_Number"],
                        f"Balance running low .Please top-up .Remaining Balance : {check_uniwallet_sms_balance}"
                    ) # Send notifications to admins and managers

            else:
                print(f"{check_uniwallet_sms_balance=}")
                self.request.session.update(
                    {
                        "sms_dictionary":{
                            "id":"uniwallet",
                            "balance":check_uniwallet_sms_balance
                        }
                    }
                )
                return self.request.session


def send_sms(self,recipients:phone_number,message:str)->send_sms_using_condition_phone_number_and_msg_content:
    # try:
    #     if check_sms_balance(self)["sms_dictionary"]["id"]=="uniwallet":
    #         ...


    #         uniwallet_headers={
    #             "Content-Type": "application/json"

    #         }


    #         uniwallet_json={
    #             "api_key": UNIWALLET_SMS_API,
    #             "merchant_id": 384,
    #             "async": False,
    #             "recipients": recipients,
    #             "message": message
    #         }


    #             with post(url="http://52.89.222.13/tfsg/public/api/send",json=uniwallet_json,headers=uniwallet_headers,timeout=timeout) as send_otp_message_using_uniwallet:
    #                 ...

    #     else:
    #         ...


    #         jasmine_headers={
    #             "Content-Type": "application/json",
    #             "Authorization":f"Basic {auth_token}"
    #         }


    #         jasmine_json={
    #             "from": "DDS GHANA",
    #             "dlr": "no",
    #             "to": recipients,
    #             "content": message
    #         }

    #         with post(url="http://66.228.38.61:8080/secure/send",json=jasmine_json,headers=jasmine_headers,timeout=timeout) as send_otp_message_using_jasmine:
    #             ...


    # except exceptions.ConnectionError:
    #     ...
    #     print("Connection Error: Can't get sms balance")
    #     print("Connection Error: Can't send either otp/ voucher to user")
                                
    #     self.request.session.update( #*
    #         {
    #             "sms_status":{"otp":None,"voucher":None,"notify-admins-and-managers":None} #*
    #         }
    #     ) #*



    uniwallet_headers={
        "Content-Type": "application/json"

    }


    uniwallet_json={
        "api_key": UNIWALLET_SMS_API,
        "merchant_id": 384,
        "async": False,
        "recipients": recipients,
        "message": message
    }

    with post(url="http://52.89.222.13/tfsg/public/api/send",json=uniwallet_json,headers=uniwallet_headers,timeout=timeout) as send_otp_message_using_uniwallet:
        ...
        print(send_otp_message_using_uniwallet.json())
        print(f'{uniwallet_json["recipients"]} - {uniwallet_json["message"]}')
