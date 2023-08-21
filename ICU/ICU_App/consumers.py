'''
WebSocket - 비동기 통신
    AI server:
              0)영상 수신 1)딥러닝 모델 로드 2)이상행동 탐지 3)탐지 내용 웹 서버에 알림
    Web server:
              0)영상 수신 1)영상 송출(브라우저) 3)AI 서버 알림 수신 후 알림창 표시(브라우저) 4)메일 발송
'''
import json
import aiohttp
import logging
import base64
import time
import numpy as np
import cv2
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import StreamingHttpResponse
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from AI_Server import ai_logic_yolo

# WebSocket 경로(live_alert.js에서 생성)
AI_SERVER_URL = "ws://127.0.0.1:8000/ws/AIserver_ws/"
WEB_SERVER_URL = "ws://127.0.0.1:8000/ws/WEBserver_ws/"

logger = logging.getLogger(__name__)


class WebServerConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.cap = None

    async def connect(self):
        self.cap = cv2.VideoCapture(
            "/Users/hui-ryung/Desktop/Project/KEB_ICU/ICU/ICU_App/hammer_horizontal_4.mp4")
        if not self.cap.isOpened():
            logger.error("Failed to open the video file.")
            return
        await self.accept()  # 웹소켓 연결 수락
        logger.info("WebSocket connection established")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                logger.warning("Failed to receive a frame from the video source")
                break
            _, buffer = cv2.imencode('.jpg', frame)
            logger.info("Received a frame from the video source")
            base64_frame = base64.b64encode(buffer).decode('utf-8')
            await self.send(text_data=json.dumps({"frame": base64_frame}))

    async def disconnect(self, close_code):
        self.cap.release()  # 카메라 해제
        logger.info("WebSocket connection closed")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if 'alert' in data:
                # AI 서버로부터의 알림 수신
                await self.send(text_data=json.dumps({'alert': True, 'message': "Anomaly detected!"}))
            elif 'mail' in data:
                # 메일 발송 요청 수신
                await self.send_mail(data['mail'])
        except Exception as e:
            print(f"Error in WebServerConsumer.receive: {e}")
    # async def start_sending_frames(self):
    #     while True:
    #         await self.get_camera_frame()
    #         if self.frame_buffer is not None and self.frame_buffer.size > 0:
    #             await self.send_frame_to_browser()
    #         await sync_to_async(time.sleep)(0.03)

    # 메일 발송 함수. mail_data에는 메일의 제목, 내용, 발신자, 수신자 리스트 등의 정보가 포함되어야 함.
    async def send_mail(self, mail_data):
        await database_sync_to_async(send_mail)(
            mail_data['subject'],
            mail_data['message'],
            mail_data['from_email'],
            mail_data['to_email_list'],
            fail_silently=False
        )


class AIServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    # async def receive(self, text_data):
    #     try:
    #         frame_bytes = text_data.encode()
    #         frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), -1)
    #         detected_classes, _ = ai_logic_yolo.process_frame(frame)
    #
    #         for detected_class in detected_classes:
    #             if self.detect_anomaly(detected_class):
    #                 await self.notify_web_server(detected_class)
    #                 await self.notify_local_environment(detected_class)
    #
    #         await self.send(text_data=json.dumps({'result': detected_classes}))
    #     except Exception as e:
    #         print(f"Error in AIServerConsumer.receive: {e}")

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


class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    # WebSocket으로부터 메시지 처리
    async def receive(self, text_data):
        data = json.loads(text_data)

        # offer가 수신되면 처리 후 answer로 응답
        if 'offer' in data:
            offer = data['offer']

            # offer 처리, answer 얻음
            answer = self.handle_offer(offer)
            await self.send(text_data=json.dumps({'answer': answer}))

        # # ICE 후보 처리
        # elif 'iceCandidate' in data:
        #     ice_candidate = data['iceCandidate']
        #     self.handle_ice_candidate(ice_candidate)

    def handle_offer(self, offer):
        # offer를 처리 원격 설명으로 설정 후 응답
        # placeholder answer만 반환하는 예시 - 수정예정
        return {
            'type': 'answer',
            'sdp': 'placeholder_sdp'
        }

    def handle_ice_candidate(self, ice_candidate):
        # 단순히 출력 예제
        print(f"받은 ICE 후보: {ice_candidate}")