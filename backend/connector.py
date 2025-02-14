from os import getcwd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


FILE=getcwd()



CAMBIUM_URL="https://kanesh.chillzone.xyz"

sms_balance_dictionary=dict(jasmine=None,uniwallet=None)
validation_dictionary=dict()
debug_dictionary=dict()
set_credentials=[] #*
voucher_balance=dict(
    total_data=None,
    used_data=None,
    usage_chart=None
)

# expired_otp_msg=dict()

# ==================
uniwallet_dictionary=dict[str,str]
send_sms_using_condition_phone_number_and_msg_content=str|dict
process_transactions=dict
phone_number=str
otp=str
voucher=str
get_balance_of_either_uniwallet_or_jasmin=str
# =================

def store_in_transactions_db(Full_Name:str,Phone_Number:str,Data_Bundle:str,Voucher_Code:str,mtnTransactionId:str,Payment_Status:bool,Voucher_Code_Recieved:bool):
    ...
    from .models import TransactionsDB

    print("Start🔴",Full_Name,Phone_Number,Data_Bundle,Voucher_Code,mtnTransactionId,Payment_Status,Voucher_Code_Recieved)
    TransactionsDB.objects.create(
        Full_Name = Full_Name,
        Phone_Number = Phone_Number,
        Data_Bundle = Data_Bundle,
        Voucher_Code = Voucher_Code,
        mtnTransactionId = mtnTransactionId,
        Payment_Status = Payment_Status,
        Voucher_Code_Recieved = Voucher_Code_Recieved,
    )

    print("End🟢✅❌")

def update_voucherdb_claimed_status_to_true(username,password):
    ...
    from .models import VouchersDB
    get_claimed_status = VouchersDB.objects.filter(username=username,password=password,claimed=False)
    if get_claimed_status.exists() == True:
        ...
        get_claimed_status.update(claimed=True)

def send_unclaimed_voucher_to_user():
    ...
    from .models import VouchersDB
    get_unclaimed_vouchers = VouchersDB.objects.filter(claimed=False).last()
    return get_unclaimed_vouchers

if __name__=="__main__":
    print(f"{FILE =}")
    print("ENV_FILE : ",BASE_DIR/"ENV_FILE.env")

