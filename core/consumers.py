from threading import Thread
from asgiref.sync import async_to_sync
from datetime import datetime
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer,JsonWebsocketConsumer
from json import loads,JSONDecodeError
from channels.layers import get_channel_layer
from requests import exceptions
from sqlite3 import Connection
from core import DATABASES


class transactions_status(JsonWebsocketConsumer):
    ...
    # channel_layer_alias = "redis"

    channel_layer_alias = "mem"
    def receive_json(self, content, **kwargs):

        self.group_name = "transactions_status"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        return super().receive_json(content, **kwargs)


    def transactions_status(self,event):
        ...
        message = event["message"]
        print(message)
        
        self.send_json(
            message
        )

