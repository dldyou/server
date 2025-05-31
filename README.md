# 모바일프로그래밍 25-1 팀 프로젝트
모바일 앱에서 사용할 AI 기능을 제공하기 위한 Flask 기반의 REST API 서버입니다.

// 아직 배포 이전입니다. 

EC2 인스턴스에 배포되어 있으며, HTTP 요청을 통해 AI 기능을 사용할 수 있습니다. 

[클라이언트] -> [nginx:80/443] -> [gunicorn:8000] -> [Flask] 의 구조로 배포하여 nginx와 gunicorn이 요청을 중간에서 관리합니다.

// 아직 배포 이전입니다.

## 일기 감정 분석 웹 서비스
- https://huggingface.co/jeonghyeon97/koBERT-Senti5 의 모델을 사용하여 일기 감정 분석
- 화남, 두려움, 행복, 평온, 슬픔 5가지 감정 분류

### 일기 감정 분석 `POST /predict`
`BODY`
```json
{
    "text": "일기 내용..."
}
```
`200 OK`
```json
{
    "predicted_label": "Happy",
    "predicted_label_id": 2,
    "probabilities": {
        "Angry": 0.056,
        "Fear": 0.2169,
        "Happy": 0.3497,
        "Sad": 0.134,
        "Tender": 0.2435
    },
    "text": "일기 내용..."
}
```
`400 BAD REQUEST`
```json
{
    "error": "No text provided"
}
```