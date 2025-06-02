import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from flask import Flask, request, jsonify
from transformers import AutoTokenizer, BertForSequenceClassification
import torch
import torch.nn.functional as F

# Load tokenizer and model from local directories
tokenizer = AutoTokenizer.from_pretrained('../tokenizer_kobert', trust_remote_code=True)
model = BertForSequenceClassification.from_pretrained('../model_kobert', num_labels=5, trust_remote_code=True)

# GPU 사용 가능하면 GPU로
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# 감정 레이블 이름 (필요 시 수정)
label_names = ["Angry", "Fear", "Happy", "Tender", "Sad"]

# Flask 서버 생성
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # 토큰화 및 텐서 변환
    inputs = tokenizer([text], return_tensors='pt', padding=True, truncation=True).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=-1).squeeze().cpu().tolist()
        pred_label_id = int(torch.argmax(logits, dim=-1).item())

    return jsonify({
        "text": text,
        "predicted_label_id": pred_label_id,
        "predicted_label": label_names[pred_label_id],
        "probabilities": {label_names[i]: round(p, 4) for i, p in enumerate(probs)}
    })

if __name__ == "__main__":
    app.run(debug=False)
