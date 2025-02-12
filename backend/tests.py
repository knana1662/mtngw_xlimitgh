from django.test import TestCase
from backend.models import UserDB
import uuid 
from django.test.utils import setup_test_environment
from django.test import Client

# setup_test_environment()

client = Client()

# # Create your tests here.

class test_UserDB(TestCase):
    # userdb=UserDB.objects.create(
    #     id=uuid.uuid4(),
    #     Full_Name="Nana Kwame Asante Danso",
    #     Phone_Number="0502270405",
    #     Data_Bundle="0.1_GHS__10MB"
    # )
    def create_UserDB(self):
        
        # UserDB.objects.latest(
        #     # Full_Name="Nana Kwame Asante Danso",
        #     # Phone_Number="0502270405",
        #     # Data_Bundle="0.1_GHS__10MB"   
        #     "Phone_Number" 
        # )

        self.assertEquals("0502270405","0502270405")

    c = Client()
    index = c.post('/', {
        "Full_Name":"Nana Kwame Asante Danso",
        "Phone_Number":"0502270405",
        "Data_Bundle":"0.11_GHS__10MB"
    })
    index.content

    otp = c.get(
        # '/otp', {
        #     "otp":"111222" 
        # }
        "/otp/?otp=718209"
    )
    otp.templates