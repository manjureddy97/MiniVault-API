# MiniVault API

A lightweight local REST API that simulates ModelVault's core feature: receiving a prompt and returning a generated response — either a   **stubbed** reply or a **real LLaMA 3-based** answer using [Ollama](https://ollama.com/).

## ✅ Features

- **POST /generate** – Stubbed (hardcoded) response generator
- **POST /generate-llama** – Real response using local LLaMA 3 model (via Ollama)
- **GET /health** – API health check
- **Logging** – All prompt/response pairs logged to `logs/log.jsonl`
- **FastAPI** – Modern framework with auto-generated API docs
- **Offline Capable** – No external cloud APIs used


## 🚀 Quick Start

### 🔧 Prerequisites

- Python 3.8+
- pip
- [Ollama](https://ollama.com/) installed and running locally with `llama3` model pulled:
  
### Setup

1. **Install dependencies**:
# Install Ollama
brew install ollama
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. **Run the API**:
 uvicorn app:app --reload
# Start Ollama
ollama run llama3.1:8b

# Pull the llama3 model (used by the API)
 ollama pull phi3:mini
 
3. **API will be available at**: `http://localhost:8000`

4. **View API docs**: `http://localhost:8000/docs`

## Usage

### Using cURL
\`\`\`bash
curl -X POST "http://localhost:8000/generate" \\
     -H "Content-Type: application/json" \\
     -d '{"prompt": "Explain machine learning"}'
\`\`\`

### Using Python
\`\`\`python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={"prompt": "What is AI?"}
)
print(response.json())
\`\`\`

### Response Format
\`\`\`json
{
  "response": "Generated response text..."
}
\`\`\`

## API Endpoints

- **POST /generate**: Generate response for prompt
- **GET /health**: Check API health
- **GET /**: API information

## Logging

All interactions are logged to `logs/log.jsonl`:
\`\`\`json
{"timestamp": "2024-01-15T10:30:00", "prompt": "Hello", "response": "Response..."}
\`\`\`

## Implementation Notes

### Current Implementation
- **Stubbed Responses**: Intelligent responses that vary based on prompt content
- **File Logging**: JSONL format for easy parsing
- **Input Validation**: Prompt validation and error handling
- **FastAPI**: Automatic API documentation and type validation

### Design Decisions
1. **FastAPI over Flask**: Better type validation and auto-docs
2. **JSONL Logging**: Easy to parse, append-friendly format
3. **Stubbed Responses**: Provides variety without requiring local models
4. **Simple Structure**: Minimal files for easy understanding and deployment

### Future Improvements
- **Local LLM Integration**: Add Hugging Face Transformers or Ollama
- **Streaming**: Token-by-token response streaming
- **Authentication**: API key protection
- **Rate Limiting**: Request throttling
- **Model Selection**: Multiple model options

## Optional Enhancements

### Local Model Integration (Bonus)
To use real models instead of stubbed responses:

\`\`\`bash
# Install transformers
pip install transformers torch

# Update app.py to use real models
from transformers import pipeline
generator = pipeline("text-generation", model="gpt2")
\`\`\`

### Streaming Support (Bonus)
Add streaming endpoint for real-time responses:

\`\`\`python
from fastapi.responses import StreamingResponse

@app.post("/generate/stream")
async def generate_stream(request: PromptRequest):
    # Implementation for streaming responses
    pass
\`\`\`

---

**Time Investment**: ~1 hour (basic version)
**Architecture**: Simple, single-file FastAPI application
**Ready for**: Local LLM integration, streaming, and production deployment
\`\`\`
