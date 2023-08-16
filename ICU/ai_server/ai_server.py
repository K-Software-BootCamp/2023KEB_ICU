import ultralytics as YOLO
from flask import Flask, request, jsonify
import torchvision
import requests
import numpy as np
import cv2
from flask_cors import CORS
from ICU.ai_server.ai_logic import process_frame

model = YOLO("/Users/hui-ryung/Desktop/Project/KEB_ICU/ICU/ai_server/models")
model.eval()

app = Flask(__name__)


@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']  # 웹캠에서 받은 프레임
    image = torchvision.transforms.ToPILImage()(file.read())  # 프레임을 이미지로 변환
    results = model(image)

    detected = len(results.pred[0]) > 0
    if detected:
        # 웹 서버에 알림 전송
        requests.post("http://127.0.0.1:8000/notify", json={"anomaly": True})

        # 싱글보드 컴퓨터에 알림 전송
        # requests.post("http://SINGLEBOARD_IP:PORT/alert", json={"anomaly": True})

    return jsonify({"anomaly": detected})


def convert_message_to_frame(message):
    # 바이트 데이터를 numpy 배열로 변환
    nparr = np.frombuffer(message, np.uint8)

    # cv2.imdecode 함수를 사용하여 numpy 배열을 이미지로 변환
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return frame


async def handle_client(client, path):
    global connected
    connected.add(client)
    try:
        async for message in client:
            frame = convert_message_to_frame(message)
            processed_frame = process_frame(frame)
            await client.send(processed_frame)
    except:
        pass
    finally:
        connected.remove(client)

# 모든 도메인 접근 허용
CORS(app)
# 접근 허용 도메인 지정
#CORS(app, resources={r"/analyze": {"origins": "http://your_specific_domain_or_ip"}})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
