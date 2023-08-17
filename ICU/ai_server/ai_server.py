import numpy as np
import cv2
from flask_cors import CORS
from ICU.ai_server.ai_logic import process_frame


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


# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000)
