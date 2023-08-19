from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseServerError
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import cv2
import json
import sys
import os

from django.views.decorators.csrf import csrf_exempt


global_buffer = None  # 전역 버퍼로 AI로부터 받은 영상 저장

'''
    Web Server : Web Page 뷰와 관련된 함수
    1) 로컬환경으로부터 웹캠 수신
    2) AI 서버로부터 알림 받으면 웹 브라우저에 알림(웹브라우저에 알림창, 메일 발송) 처리
'''

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
    #print(request)  # 요청에서 받은 파일의 내용을 출력 - 테스트용
    try:
        file = request.FILES['file'].read()
        #print(request.FILES['file'].read())
        if not file:
            raise ValueError("No 'file' in request.FILES")

        return StreamingHttpResponse(generate(file), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print("Error(views.live_feed):", e)
        return HttpResponseServerError(str(e))


# # 웹 페이지 렌더링
# def main(request):
#     return render(request, 'ICU/live_stream.html')


@csrf_exempt
def ai_stream(request):
    global global_buffer
    if request.method == 'POST':
        global_buffer = request.FILES['file'].read()
    return JsonResponse({"status": "OK"})


# AI 서버 알림 처리
@csrf_exempt
def notify(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if data["anomaly"]:
            # 사용자에게 웹소켓을 통한 알림 전송
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "alerts",
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
