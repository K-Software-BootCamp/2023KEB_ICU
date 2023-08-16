from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ICU.ai_server.ai_logic import process_frame
import cv2
import requests
import json


AI_SERVER_URL = "http://127.0.0.1:5000/analyze"


# 카메라에서 읽어온 프레임 스트리밍
def gen(camera):
    while True:
        frame = camera.read()
        frame_processed = process_frame(frame)
        ret, jpeg = cv2.imencode('.jpg', frame_processed)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            continue


# 비디오 카메라 제어 클래스
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)  # 0 for default camera

    def __del__(self):
        self.video.release()

    def read(self):
        ret, frame = self.video.read()
        return frame


# 실시간 피드 스트리밍
def live_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")


# 웹 페이지 렌더링
def main(request):
    return render(request, 'ICU/live_stream.html')


# /analyze 경로에 이미지 전송 및 AI 서버 응답 처리
def generate():
    global old_frame
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_bytes = cv2.imencode(".jpg", frame)[1].tobytes()

        try:
            response = requests.post(AI_SERVER_URL, files={"file": frame_bytes})
            response.raise_for_status()  # 응답 코드가 오류를 나타내면 예외 발생

            # JSON 데이터 확인
            if response.headers.get("content-type") == "application/json":
                data = response.json()

                # data가 올바른 형태인지 ("anomaly" 키를 포함하는지) 확인
                if "anomaly" in data and data["anomaly"]:
                    if old_frame is not None:
                        frame = old_frame
                else:
                    old_frame = frame

            else:
                print("Invalid response from AI server:", response.text)

        except requests.RequestException as e:
            print("Error during request:", e)
        except json.JSONDecodeError:
            print("Invalid JSON response:", response.text)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()


# AI 서버 알림 처리
def notify(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if data["anomaly"]:
            # 사용자에게 웹소켓을 통한 알림 전송
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "alerts",  # Group name
                {
                    "type": "alert.message",
                    "message": "Anomaly detected!",
                },
            )

            # 이메일 알림 전송 (Django 이메일 기능 사용)
            from django.core.mail import send_mail
            send_mail(
                'Anomaly Detected',
                'Anomaly detected by CCTV!',
                'from_email@example.com',
                ['admin@example.com'],
                fail_silently=False,
            )

    return JsonResponse({"status": "OK"})