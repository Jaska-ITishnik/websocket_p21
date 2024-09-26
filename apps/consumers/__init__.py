from apps.consumers.main import ChatConsumer
#
# class ChatConsumer(AsyncJsonWebsocketConsumer):
#
#     async def check_user(self) -> None:
#         if self.user.is_anonymous:
#             await self.send_json({"message": "Login is required!"})
#             await self.disconnect(0)
#             await self.close()
#
#     async def status_notification(self, is_active: bool = True):
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "chat.message",
#                 "message": f"{self.user.username} is {('offline', 'online')[is_active]}",
#                 "from_user": model_to_dict(self.user, ['id', 'username'])
#             }
#         )
#
#     async def connect(self):
#         self.user = self.scope['user']
#         self.partner_id = self.scope['url_route']['kwargs']['id']
#         self.group_name = (
#             f'chat_{self.user.id}_{self.partner_id}'
#             if int(self.user.id) > int(self.partner_id)
#             else f'chat_{self.partner_id}_{self.user.id}')
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.check_user()
#         await self.accept()
#
#     async def disconnect(self, code):
#         await self.status_notification(False)
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)
#
#     async def receive_json(self, content, **kwargs):
#         message = content['message']
#         msg = await Message.objects.acreate(reciver_id=self.partner_id, message=message, author=self.user)
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "chat.message",
#                 "message": model_to_dict(msg, ['id', 'message']),
#                 "from_user": model_to_dict(self.user, ['id', 'username'])
#             }
#         )
#
#     async def chat_message(self, event):
#         response = {
#             'message': event['message']['message'] if isinstance(event['message'], dict) else event['message'],
#             'from_user': event['from_user']['username']
#         }
#         if self.user.id != event['from_user']['id'] and str(self.partner_id) in self.group_name.split('_')[1:]:
#             await self.send_json(response)
#         else:
#             if isinstance(event['message'], dict):
#                 await self.send_json(event['message'] | {"status": "Send message!"})
# work with files
# class CustomAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
#
#     async def receive(self, text_data=None, bytes_data=None, **kwargs):
#         try:
#             ujson.loads(text_data)
#         except JSONDecodeError:
#             await self.send_json({"message": "Send message in json format!"})
#         else:
#             return await super().receive(text_data, bytes_data, **kwargs)
#
#     @classmethod
#     async def decode_json(cls, text_data):
#         return ujson.loads(text_data)
#
#     @classmethod
#     async def encode_json(cls, content):
#         return ujson.dumps(content)
#
# class ChatConsumer(CustomAsyncJsonWebsocketConsumer):
#     group_name = 'chat'
#
#     async def save_msg(self, content) -> Message:
#         return await Message.objects.acreate(
#             message=content.get('message'),
#             author=self.user,
#             file_id=content.get('file')
#         )
#
#     async def check_user(self) -> bool:
#         if self.user.is_anonymous:
#             await self.send_json({'message': 'login is required!'})
#             await self.disconnect(0)
#             await self.close()
#             return False
#         return True
#
#     async def notify_status(self, is_connected: bool = True) -> None:
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "notification.message",
#                 "message": f"{self.user.username} is {('offline', 'online')[is_connected]} !",
#                 "from_user": model_to_dict(self.user, ['id', 'username']),
#             }
#         )
#
#     async def connect(self) -> None:
#         self.user = self.scope['user']
#         # Join room group
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()
#
#         if not await self.check_user():
#             return
#         await self.notify_status()
#
#     async def disconnect(self, close_code):
#         # Leave room group
#         if self.user.is_authenticated:
#             await self.notify_status(False)
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)
#
#     # Receive message from WebSocket
#     async def receive_json(self, content, **kwargs):
#         keys = {'message', 'file'}
#         if len(set(content) & keys) < 1:
#             await self.send_json({'message': f'Shu kalitlardan birini yuborish shart {keys}'})
#             return
#         if not isinstance(content, dict):
#             await self.send_json({"message": "Send message in json format!"})
#
#         # Send message to room group
#         msg = await self.save_msg(content)
#
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "chat.message",
#                 "message": model_to_dict(msg, ['id', 'message', 'file']),
#                 "from_user": model_to_dict(self.user, ['id', 'username']),
#             }
#         )
#
#     async def notification_message(self, event):
#         response = {
#             "message": event.get('message'),
#             "file": event.get('file'),
#             "from_user": event["from_user"]['username']
#         }
#         if self.user.id != event["from_user"]['id']:
#             await self.send_json(response)
#         else:
#             await self.send_json(
#                 {
#                     "message": event['message'],
#                     "status": "xabar yuborildi"
#                 }
#             )
#
#     # Receive message from room group
#     async def chat_message(self, event):
#         # Send message to WebSocket
#         response = {
#             "message": event["message"]['message'],
#             "file": event['message']['file'],
#             "from_user": event["from_user"]['username']
#         }
#         if self.user.id != event["from_user"]['id']:
#             await self.send_json(response)
#         else:
#             await self.send_json(event['message'] | {"status": "xabar yuborildi"})
# one to one chat
