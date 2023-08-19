import numpy as np
import cv2
import io
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jsonify.convert import jsonify

from ICU.AI_Server import ai_logic_yolo
from ICU.AI_Server.ai_logic_yolo import process_frame, model
from PIL import Image

'''
    AI Server
    1) 로컬환경으로부터 웹캠 수신
    2) 이상행동 탐지시 웹서버와 로컬환경으로 알림 전송
'''

AI_SERVER_URL = "ws://127.0.0.1:8001/AIserver_ws/"


# 이미지를 모델로 분석 후 결과 반환
@csrf_exempt
def receive_webcam(request):
    if request.method == "POST":
        file = request.FILES["file"].read()
        detected_classes, _ = ai_logic_yolo.process_frame(file.read())

        # 이상 행동 판단
        for detected_class in detected_classes:
            if detect_anomaly(detected_class):
                # 웹 서버 및 Local_Environment에 알림
                notify_web_server(detected_class)
                notify_local_environment(detected_class)

        return JsonResponse({"results": detected_classes})


def detect_anomaly(result):
    anomalous_objects = ["knife", "fist", "hammer"]
    return result in anomalous_objects


# 웹 서버에 알림을 전송
def notify_web_server(detected_class):
    url = "YOUR_WEB_SERVER_URL/notify"
    data = {"message": f"Anomaly Detected! Object: {detected_class}"}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to notify web server: {response.text}")
    return response.ok


# Local_Environment에 알림을 전송
def notify_local_environment(detected_class):
    url = "YOUR_LOCAL_ENVIRONMENT_URL/notify"
    data = {"message": f"Anomaly Detected! Object: {detected_class}"}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to notify web server: {response.text}")
    return response.ok
