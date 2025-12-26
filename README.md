# Logikey 🧠

**Logikey** is an AI-powered backend infrastructure designed to detect and analyze logical fallacies in arguments. Built with **FastAPI** and powered by the **Llama 3 8B** large language model, Logikey provides structured analysis, in-depth explanations, and counter-argument suggestions.

This project is specifically developed to support integration with smart keyboard applications, helping users communicate with stronger logic.

## ✨ Key Features

- **Automated Fallacy Detection**: Instantly identifies various types of logical errors.
- **Structured Analysis**: Provides fallacy labels, rational explanations, and argument validity status.
- **Counter-Argument Generation**: Generates counter-argument points to weaken detected fallacies.
- **Sensitivity Control**: Adjustable analysis sensitivity (Critical vs. Relaxed) affecting the model's logical rigor.
- **Security**: Equipped with API Key validation for endpoint access.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI Model**: [Meta Llama 3 8B Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct)
- **Adapter**: [Logikey Llama 3 Adapter](https://huggingface.co/sovvaaz/Logikey-llama3-adapter) (Custom Adapter via PEFT)
- **AI Libraries**: `transformers`, `torch`, `peft`, `bitsandbytes` (for 8-bit quantization)
- **Infrastructure**: Docker, Python 3.10+

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- NVIDIA GPU (Recommended for optimal performance via CUDA)
- Hugging Face Access Token (with access to Llama 3)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/username/Logikey.git
   cd Logikey
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   HF_TOKEN=your_huggingface_token
   MODEL_PATH=sovvaaz/Logikey-llama3-adapter
   APP_SECRET_KEY=your_secure_api_key
   ```

5. **Run the Server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## 🐳 Using Docker

You can also run Logikey using Docker:

```bash
docker build -t Logikey-api .
docker run -p 8000:8000 --gpus all --env-file .env Logikey-api
```

## 📖 API Documentation

### 1. Analyze Argument
**Endpoint:** `POST /analyze`

**Headers:**
- `X-API-Key`: `<APP_SECRET_KEY>`

**Request Body:**
```json
{
  "text": "Everyone is using this product, so it must be the best.",
  "sensitivity": 0.8
}
```

**Response:**
```json
{
  "input": "Everyone is using this product, so it must be the best.",
  "label": "Bandwagon Fallacy",
  "explanation": "This argument claims something is true simply because it is popular.",
  "is_fallacy": true,
  "counter_arguments": [
    "Popularity does not guarantee quality.",
    "Many things popular in the past were later proven scientifically wrong."
  ],
  "status": "success",
  "sensitivity": 0.8
}
```

### 2. Health Check
**Endpoint:** `GET /health`
Used to check server readiness and model status (CUDA/CPU).

## 🧩 Contributing
Contributions are welcome! Please open an issue or submit a pull request if you want to improve model accuracy or add new features.
