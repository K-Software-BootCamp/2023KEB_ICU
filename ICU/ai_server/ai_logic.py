import cv2
import torch
import supervision as sv
from ultralytics import YOLO

# 모델 초기화
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = YOLO("/Users/hui-ryung/Desktop/Project/KEB_ICU/ICU/ai_server/models/best_custom.pt")  # 파일 경로


# 프레임 처리
def process_frame(frame):
    box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=2, text_scale=1)
    results = model.predict(frame)[0]
    classes = ["fist", "hammer", "knife"]
    detections = sv.Detections.from_yolov8(results)
    high_confidence_detections = detections[detections.confidence >= 0.6]
    labels = [f"{classes[class_id]} {confidence:0.2f}" for _, _, confidence, class_id, _ in high_confidence_detections]
    img = frame
    img = box_annotator.annotate(scene=img, detections=high_confidence_detections, labels=labels)
    if img is None:
        print("Image is None")
    small_img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    return small_img