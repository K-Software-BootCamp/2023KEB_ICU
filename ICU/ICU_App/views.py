from django.shortcuts import render
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
import json
import cv2


from django.views.decorators.csrf import csrf_exempt

global_buffer = None  # 전역 버퍼로 AI로부터 받은 영상 저장

'''
    Web Server : Web Page 뷰와 관련된 함수
    1) 로컬환경으로부터 웹캠 수신
    2) AI 서버로부터 알림 받으면 웹 브라우저에 알림(웹브라우저에 알림창, 메일 발송) 처리
    -> 현재 consumer에서 작동하도록 수정(web socket)
'''


def main(request):
    return render(request, 'ICU/live_stream.html')


# @csrf_exempt
# def ai_stream(request):
#     global global_buffer
#     if request.method == 'POST':
#         global_buffer = request.FILES['file'].read()
#     return JsonResponse({"status": "OK"})
#
#
# # AI 서버 알림 처리
# @csrf_exempt
# def notify(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))
#         if data["anomaly"]:
#             # 사용자에게 웹소켓을 통한 알림 전송
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 "alerts",
#                 {
#                     "type": "alert.message",
#                     "message": "Anomaly detected!",
#                 },
#             )
#
#             # 이메일 알림 전송 (Django 이메일 기능 사용)
#             from django.core.mail import send_mail
#             send_mail(
#                 'Anomaly Detected',
#                 'Anomaly detected by CCTV!',
#                 'from_email@example.com',
#                 ['admin@example.com'],
#                 fail_silently=False,
#             )
#     return JsonResponse({"status": "OK"})
#
#
# def capture_and_send():
#     cap = cv2.VideoCapture("/Users/hui-ryung/Desktop/Project/KEB_ICU/ICU/AI_Server/test_video/hammer_horizontal_4.mp4")
#
#     while True:
#         ret, frame = cap.read()
#
#         if not ret:
#             print("Failed to grab frame")
#             break
#
#         frame_bytes = cv2.imencode(".jpg", frame)[1].tobytes()
#
#         try:
#             # AI 서버로 프레임 전송
#             send_frame_to_server("ai_server_group", frame_bytes)
#             print(f"Sent frame to AI server")
#
#             # 웹 서버로 프레임 전송
#             send_frame_to_server("web_server_group", frame_bytes)
#             print(f"Sent frame to Web server")
#
#             # 웹 브라우저로 프레임 전송
#             send_frame_to_server("browser_group", frame_bytes)
#             print(f"Sent frame to browser")
#
#             # # AI 서버의 응답을 확인하여 알림 처리
#             # if "anomaly" in response_ai and response_ai["anomaly"]:
#             #     print("Anomaly detected! Sending alert...")
#             #     # 스피커로 알림 전송(대체 예정)
#             #     # pygame.init()
#             #     # alert_sound = pygame.mixer.Sound('alert_sound_file_path.wav')
#             #     # alert_sound.play()
#         except Exception as e:
#             print("Error during request:", e)
#
#     cap.release()