'''
WebSocket
Channels와 함께 실시간 통신 위해 사용
'''
import json
import aiohttp
import numpy as np
import cv2
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from AI_Server import ai_logic_yolo
from django.http import StreamingHttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

AI_SERVER_URL = "ws://127.0.0.1:8000/ws/AIserver_ws/"
WEB_SERVER_URL = "ws://127.0.0.1:8000/ws/WEBserver_ws/"
BROWSER_URL = "ws://127.0.0.1:8000/ws/BROWSERserver_ws/"

# 비동기 웹소켓 컨슈머

class WebServerConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_buffer = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    # 프레임 받아오기
    async def receive(self, text_data):
        try:
            frame_bytes = text_data.encode()
            self.frame_buffer = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), -1)
            await self.send_frame()
        except Exception as e:
            print(f"Error in WebServerConsumer.receive: {e}")

    # 프레임 보내기
    async def send_frame(self):
        if self.frame_buffer is not None:
            frame_encoded = cv2.imencode('.jpg', self.frame_buffer)[1].tobytes()
            await self.send(text_data=frame_encoded)
            self.frame_buffer = None

    @csrf_exempt
    # 카메라에서 읽어온 프레임 스트리밍 및 웹 브라우저로 전송
    def generate(file):
        global global_buffer

        while True:
            if global_buffer:
                frame_bytes = global_buffer
                global_buffer = None
            else:
                frame_bytes = file
            yield (b'--frame\\r\\n'
                   b'Content-Type: image/jpeg\\r\\n\\r\\n' + frame_bytes + b'\\r\\n\\r\\n')

    @csrf_exempt
    # 실시간 피드 스트리밍
    def live_feed(request):
        # print(request)  # 요청에서 받은 파일의 내용을 출력 - 테스트용
        try:
            file = request.FILES['file'].read()
            # print(request.FILES['file'].read())
            if not file:
                raise ValueError("No 'file' in request.FILES")

            return StreamingHttpResponse(request.generate(file), content_type="multipart/x-mixed-replace;boundary=frame")
        except Exception as e:
            print("Error(views.live_feed):", e)
            return HttpResponseServerError(str(e))


class AIServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            frame_bytes = text_data.encode()
            frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), -1)
            detected_classes, _ = ai_logic_yolo.process_frame(frame)

            for detected_class in detected_classes:
                if self.detect_anomaly(detected_class):
                    await self.notify_web_server(detected_class)
                    await self.notify_local_environment(detected_class)

            await self.send(text_data=json.dumps({'result': detected_classes}))
        except Exception as e:
            print(f"Error in AIServerConsumer.receive: {e}")

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
        await self.async_send_mail(detected_class)

    @database_sync_to_async
    def async_send_mail(self, detected_class):
        send_mail(
            'Anomaly Detected',
            f'Anomaly detected by CCTV! Object: {detected_class}',
            'from_email@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )

    async def notify_local_environment(self, detected_class):
        # Update this with the actual URL
        url = "localhost:8000/notify"
        data = {"message": f"Anomaly Detected! Object: {detected_class}"}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, data=data) as response:
                    if response.status != 200:
                        print(f"Failed to notify local environment: {response.text}")
                    return response.status == 200
            except Exception as e:
                print(f"Error in AIServerConsumer.notify_local_environment: {e}")


class BrowserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("browser_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("browser_group", self.channel_name)

    async def receive(self, text_data):
        # 웹캠에서 프레임 캡처
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            frame_bytes = cv2.imencode(".jpg", frame)[1].tobytes()

            # AI 서버로 프레임 전송
            response_ai = await self.send_frame_to_channel(AI_SERVER_URL, frame_bytes)
            print(f"Received response from AI server: {response_ai}")

            # 웹 서버로 프레임 전송
            response_web = await self.send_frame_to_channel(WEB_SERVER_URL, frame_bytes)
            print(f"Received response from Web server: {response_web}")
            # 웹 브라우저로 프레임 전송
            await self.send(text_data=frame_bytes)
        cap.release()


async def send_frame_to_channel(self, channel_group_name, frame_bytes):
        channel_layer = get_channel_layer()
        # 채널 레이어를 사용하여 특정 그룹에 메시지 전송
        await channel_layer.group_send(
            channel_group_name,
            {
                "type": "frame.message",
                "frame": frame_bytes
            }
        )