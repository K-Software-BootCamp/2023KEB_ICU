from django.shortcuts import render


'''
메인 웹 페이지 렌더링
'''

def main(request):
    return render(request, 'ICU_App/live_stream.html', {})


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
#             # # AI 서버의 응답을 확인하여 알림 처리
#             # if "anomaly" in response_ai and response_ai["anomaly"]:
#             #     print("Anomaly detected! Sending alert...")
#             #     # 스피커로 알림 전송(대체 예정)
#             #     # pygame.init()
#             #     # alert_sound = pygame.mixer.Sound('alert_sound_file_path.wav')
#             #     # alert_sound.play()
#         except Exception as e:
#             print("Error during request:", e)