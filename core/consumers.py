from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


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

