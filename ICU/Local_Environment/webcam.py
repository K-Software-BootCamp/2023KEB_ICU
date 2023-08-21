# import cv2
# import asyncio
# import websockets
# import json
# # import pygame 스피커 알림
#
# '''
# AI_Server, Web_Server로 실시간 웹캠 전송
# '''
#
# AI_SERVER_URL = "ws://127.0.0.1:8001/AIserver_ws/"
# WEB_SERVER_URL = "ws://127.0.0.1:8002/WEBserver_ws/"
#
#
# async def send_frame_to_server(url, frame_bytes):
#     async with websockets.connect(url) as ws:
#         await ws.send(frame_bytes)
#         response = await ws.recv()
#         return json.loads(response)
#
#
# async def capture_and_send():
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
#             response_ai = await send_frame_to_server(AI_SERVER_URL, frame_bytes)
#             print(f"Received response from AI server: {response_ai}")
#
#             # 웹 서버로 프레임 전송
#             response_web = await send_frame_to_server(WEB_SERVER_URL, frame_bytes)
#             print(f"Received response from Web server: {response_web}")
#
#             # AI 서버의 응답을 확인하여 알림 처리
#             if "anomaly" in response_ai and response_ai["anomaly"]:
#                 print("Anomaly detected! Sending alert...")
#                 # 스피커로 알림 전송(대체 예정)
#                 # pygame.init()
#                 # alert_sound = pygame.mixer.Sound('alert_sound_file_path.wav')
#                 # alert_sound.play()
#         except Exception as e:
#             print("Error during request:", e)
#
#     cap.release()
#
#
# def start_webcam_capture():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(capture_and_send())
#
#
# if __name__ == "__main__":
#     start_webcam_capture()
