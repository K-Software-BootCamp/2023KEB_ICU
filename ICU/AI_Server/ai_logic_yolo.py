import cv2
import torch
import supervision as sv
from ultralytics import YOLO

'''
YOLO 객체 팀지
'''

# YOLO 객체 초기화
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print("Using", device)

# 모델 초기화
model = YOLO("/Users/hui-ryung/Desktop/Project/KEB_ICU/ICU/AI_Server/models/best_custom.pt")  # 파일 경로


# 입력 프레임(이미지) 처리하여 객체 탐지 및 상자 그림
def process_frame(frame):
    # 박스 생성
    box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=2, text_scale=1)
    classes = ["fist", "hammer", "knife"]

    # YOLOv5를 사용해 객체 감지
    yolov5_results = model.predict(frame)[0]

    # YOLOv5의 결과에서 `Detections` 객체 생성
    detections = sv.Detections.from_yolov5(yolov5_results)
    high_confidence_detections = detections[detections.confidence >= 0.6]

    detected_classes = [classes[class_id] for _, _, _, class_id, _ in high_confidence_detections]

    # 레이블
    labels = [f"{cls} {confidence:0.2f}" for _, _, confidence, class_id, _ in high_confidence_detections for cls in
              detected_classes]

    # 원본 프레임에 박스와 레이블 표시
    img = frame
    img = box_annotator.annotate(scene=img, detections=high_confidence_detections, labels=labels)
    if img is None:
        print("Image is None")

    # 리사이즈 및 반환
    small_img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    return detected_classes, small_img
