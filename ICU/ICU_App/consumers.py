'''
WebSocket
Channels와 함께 실시간 통신 위해 사용
'''
import json
import aiohttp
import numpy as np
import cv2
from channels.generic.websocket import AsyncWebsocketConsumer

from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ICU.AI_Server import ai_logic_yolo


# 비동기 웹소켓 컨슈머
class AlertConsumer(AsyncWebsocketConsumer):
    # 연결
    async def connect(self):
        await self.channel_layer.group_add("alerts", self.channel_name)
        await self.accept()

    # 연결 해제
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("alerts", self.channel_name)

    # 클라이언트에 메세지 전송
    async def alert_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @classmethod
    def as_asgi(cls):
        return cls


class AIServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        frame_bytes = text_data.encode()
        frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), -1)
        detected_classes, _ = ai_logic_yolo.process_frame(frame)

        for detected_class in detected_classes:
            if self.detect_anomaly(detected_class):
                await self.notify_web_server(detected_class)
                await self.notify_local_environment(detected_class)

        await self.send(text_data=json.dumps({'result': detected_classes}))

    def detect_anomaly(self, result):
        anomalous_objects = ["knife", "fist", "hammer"]
        return result in anomalous_objects

    async def notify_web_server(self, detected_class):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "alerts",
            {
                "type": "alert.message",
                "message": f"Anomaly detected! Object: {detected_class}",
            },
        )

        send_mail(
            'Anomaly Detected',
            'Anomaly detected by CCTV!',
            'from_email@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )

    @classmethod
    def as_asgi(cls):
        return cls()

    async def notify_local_environment(self, detected_class):
        url = "YOUR_LOCAL_ENVIRONMENT_URL/notify"
        data = {"message": f"Anomaly Detected! Object: {detected_class}"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status != 200:
                    print(f"Failed to notify local environment: {response.text}")
                return response.status == 200


class WebServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        frame_bytes = text_data.encode()
        frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), -1)
        # 웹 페이지에 프레임 표시 로직이 여기에 들어갑니다.
        await self.send(text_data=json.dumps({'result': 'some result'}))

    @classmethod
    def as_asgi(cls):
        return cls()