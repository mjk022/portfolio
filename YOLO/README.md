# 🎯 YOLO v1 논문 구현

| 항목 | 내용 |
|---|---|
| 활동 | 학회 DALC(달씨) 논문 구현 프로젝트 · 최종 발표 (2023.08, 2인 팀) |
| 논문 | Redmon et al., [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640) (2016) |
| 참고 코드 | [aladdinpersson/Machine-Learning-Collection — YOLO](https://github.com/aladdinpersson/Machine-Learning-Collection/tree/master/ML/Pytorch/object_detection/YOLO) |
| 데이터 | Pascal VOC 2007/2012 (20 클래스), 학습용 100장 샘플 `Data/100examples.csv` ([Kaggle](https://www.kaggle.com/datasets/734b7bcb7ef13a045cbdd007a3c19874c2586ed0b02b4afc86126e89d00af8d2)) |
| 도구 | PyTorch, Google Colab |

## 모델 구조

```mermaid
flowchart LR
    A[입력 이미지<br/>448×448] --> B[Darknet<br/>24 Conv + BatchNorm + LeakyReLU]
    B --> C[FC 1024·S·S → 496]
    C --> D[FC 496 → S·S·（C+B·5）]
    D --> E[7×7 격자별<br/>박스 2개 + 클래스 20개]
    E --> F[NMS]
    F --> G[최종 Bounding Box]
```

## 파일 구성

| 파일 | 역할 |
|---|---|
| `Data/getdata.ipynb` | Pascal VOC 다운로드, 라벨 변환, train/test CSV 생성 |
| `Data/dataset.ipynb` | `VOCDataset`: 이미지와 라벨을 7×7 격자 타깃 행렬로 변환 |
| `model.ipynb` | `CNNBlock`, `Yolov1` (Darknet + FC) |
| `loss.ipynb` | `YoloLoss`: 좌표 · 객체 · 비객체 · 클래스 손실 (λ_coord=5, λ_noobj=0.5) |
| `utils.ipynb` | IoU, NMS, mAP, 박스 변환, 시각화, 체크포인트 |
| `train_*.ipynb` | 학습 + 결과 시각화 (아래 3단계) |

## 구현 결과

| 단계 | 노트북 | 추가한 기능 |
|---|---|---|
| 1 | `train_bbox + class.ipynb` | 바운딩 박스에 클래스 표시 |
| 2 | `train_bbox + class + 확률.ipynb` | 클래스 + 확률값 표시 |
| 3 | `train_bbox + class + 확률 + 그래프.ipynb` | epoch별 Loss · mAP 그래프 |

**1. BBox + Class**

![스크린샷(1112)](https://github.com/mjk022/portfolio/assets/114840042/a11ab26c-17f2-4d26-ad39-7796246ca6a6)

**2. BBox + Class + 확률**

![스크린샷(1115)](https://github.com/mjk022/portfolio/assets/114840042/6e8dc329-fc8b-484c-9838-d6e5d481bb8c) ![스크린샷(1114)](https://github.com/mjk022/portfolio/assets/114840042/84250405-5ea4-4853-8c72-e925d2c358e0)

**3. Loss · mAP 그래프**

![스크린샷(1113)](https://github.com/mjk022/portfolio/assets/114840042/3be35946-8825-4606-a6e4-61d5b045250f)

## 문제 해결 기록

| # | 문제 | 해결 |
|---|---|---|
| 1 | 표시되는 확률이 1을 넘음 | `score = max(0, min(1, score))`로 클리핑 |
| 2 | 학습이 잘 되는지 한눈에 보기 어려움 | epoch별 mAP · Loss를 저장해 그래프로 시각화 |
| 3 | epoch가 중복으로 학습됨 | 학습 루프 구조 정리 |
| 4 | 테스트 평가 시 모델이 초기화됨 | `LOAD_MODEL=True`로 저장된 체크포인트를 불러와 평가 |

## 클래스 (Pascal VOC)

| 분류 | 클래스 (번호) |
|---|---|
| 탈것 | 비행기 0, 자전거 1, 배 3, 자동차 6, 오토바이 13, 기차 18 |
| 동물 | 새 2, 고양이 7, 개 11, 말 12, 사람 14, 양 16 |
| 실내 | 병 4, 의자 8, 테이블 10, 화분 15, 소파 17, 모니터 19 |
