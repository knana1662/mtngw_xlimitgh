
from routeros_api import exceptions,RouterOsApiPool
from os import getenv
# MikroTik API Credentials
host = getenv("MIKROTIK_IP")  # Change to your MikroTik router's IP
username = getenv("MIKROTIK_USERNAME")     # Change if necessary
password = getenv("MIKROTIK_PASSWORD")

########################
# Define user details
hotspot_customer = getenv("MIKROTIK_HOTSPOT_CUSTOMER")  # User Manager customer (default is "admin")
# hotspot_username = "a"
# hotspot_password = "a"
# hotspot_profile = "5 GHS@5GB valid for 24hrs"  # Ensure this profile exists


# Connect to MikroTik API
conn = RouterOsApiPool(
    host, 
    username=username, 
    password=password, 
    plaintext_login=True  # Set to False if using TLS
)

api = conn.get_api()

verify_system_identity = api.get_resource('/system/identity').get()
get_list_of_all_userman_profiles_created = api.get_resource('/tool/user-manager/profile').get()
add_user_to_userman_user = api.get_resource('/tool/user-manager/user')
get_list_of_all_userman_users_created = api.get_resource('/tool/user-manager/user').get()

def create_and_get_user(profile,hotspot_username,hotspot_password):
    ...

    list_of_all_userman_profiles_created  = [
        {
            "name":get_profile["name"],
            "validity":get_profile["validity"],
            "starts-at":get_profile["starts-at"],
            "override-shared-users":get_profile["override-shared-users"]
        }
        for idx,get_profile in enumerate(get_list_of_all_userman_profiles_created)

    ]

    for idx,hotspot_profile in enumerate(list_of_all_userman_profiles_created):
        ...
        if hotspot_profile["name"].startswith(profile):

            try:
                # 1. Create a User

                add_user_to_userman_user.add(
                    customer=hotspot_customer,
                    username=hotspot_username,
                    password=hotspot_password,
                )

                add_user_to_userman_user.call('create-and-activate-profile', {
                    'customer': hotspot_customer,
                    'numbers': hotspot_username,  # Required to specify the user
                    'profile': hotspot_profile
                })

            except exceptions.RouterOsApiCommunicationError as e:
                ...
                print(f"{e.args[-1]=}\n")

            list_of_all_userman_users_created = [
                {
                    "hotspot_user" :  get_user['username'],
                    "hotspot_password" : get_user["password"],
                    "hostpot_data_bundle" : {
                        "data": "Nan" if get_user.get("actual-profile") ==  None else get_user["actual-profile"].split(" valid for ")[0],
                        "expiry": "Nan" if get_user.get("actual-profile") ==  None else get_user["actual-profile"].split(" valid for ")[1]
                    },
                    "hotspot_shared" : get_user["shared-users"],
                    "hotspot_active" : get_user["active"]
                }

                for idx,get_user in enumerate(get_list_of_all_userman_users_created)
            ]

            for idx,created_user in enumerate(list_of_all_userman_users_created):
                if hotspot_username == created_user["hotspot_user"]:
                    ...
                    return created_user
