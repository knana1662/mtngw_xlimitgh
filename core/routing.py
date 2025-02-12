from django.urls import path,re_path

from core import transactions_status

websocket_urlpatterns = [
    path('ws/transactions_status/',transactions_status.as_asgi()), # for showing transaction status (pending,processing,success or failed)
]
