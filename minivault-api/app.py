from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import json
import os
import random
from ollama import Client


# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

app = FastAPI(
    title="MiniVault API",
    description="A lightweight local REST API for prompt generation",
    version="1.0.0"
)

# Enable CORS (optional, for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    response: str

ollama_client = Client(host='http://localhost:11434')


def log_interaction(prompt: str, response: str):
    """Log the prompt/response interaction to logs/log.jsonl"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    }
    
    try:
        with open("logs/log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Error logging interaction: {e}")

def generate_stubbed_response(prompt: str) -> str:
    """Generate a stubbed response based on the prompt"""
    
    # Different response templates based on prompt content
    if "code" in prompt.lower() or "programming" in prompt.lower():
        responses = [
            f"Here's a code example for '{prompt}':\n\n```python\nprint('Hello, World!')\n```\n\nThis demonstrates basic programming concepts.",
            f"For coding questions like '{prompt}', I'd recommend starting with fundamentals and building complexity gradually.",
        ]
    elif "explain" in prompt.lower() or "what is" in prompt.lower():
        responses = [
            f"Let me explain '{prompt}' in simple terms:\n\nThis concept involves several key components working together.",
            f"'{prompt}' can be understood by breaking it down into smaller, manageable parts.",
        ]
    elif "help" in prompt.lower() or "how to" in prompt.lower():
        responses = [
            f"I'd be happy to help with '{prompt}'. Here are some steps you can follow:",
            f"For '{prompt}', I recommend taking a systematic approach.",
        ]
    else:
        responses = [
            f"Thank you for your prompt: '{prompt}'. This is a simulated response from MiniVault API.",
            f"Based on your input '{prompt}', here's a thoughtful response from our local model.",
            f"Your prompt '{prompt}' is interesting. Let me share some insights on this topic.",
            f"Processing your request about '{prompt}'. Here's what I can tell you...",
        ]
    
    base_response = random.choice(responses)
    
    # Add some context
    elaboration = f"""

This response demonstrates MiniVault API capabilities:
• Local prompt processing
• Contextual response generation  
• Interaction logging to logs/log.jsonl
• RESTful API design with FastAPI

In production, this could be powered by:
• Hugging Face Transformers
• Ollama with Llama models
• Custom fine-tuned models

The system maintains full offline capability."""
    
    return base_response + elaboration

def generate_llama_response(prompt: str) -> str:
    """Call Ollama client to generate a response using phi3:mini model with a system prompt"""
    try:
        system_prompt = "You are a helpful AI assistant called MiniVault, designed to give clear and concise answers."

        response = ollama_client.chat(
            model="phi3:mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response['message']['content'].strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama generation failed: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MiniVault API is running!",
        "version": "1.0.0",
        "endpoints": {
            "generate": "POST /generate - Generate response for prompt",
            "health": "GET /health - Check API health"
        }
    }

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: PromptRequest):
    """Generate a response for the given prompt"""
    try:
        # Validate prompt
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        if len(request.prompt) > 5000:
            raise HTTPException(status_code=400, detail="Prompt too long (max 5000 characters)")
        
        # Generate response (stubbed)
        response = generate_stubbed_response(request.prompt.strip())
        
        # Log the interaction
        log_interaction(request.prompt.strip(), response)
        
        return GenerateResponse(response=response)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/generate-llama", response_model=GenerateResponse)
async def generate_llama(request: PromptRequest):
    """Generate a response using Ollama's phi3:mini model"""
    try:
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        if len(request.prompt) > 5000:
            raise HTTPException(status_code=400, detail="Prompt too long (max 5000 characters)")

        response = generate_llama_response(request.prompt.strip())
        log_interaction(request.prompt.strip(), response, model="phi3:mini")
        return GenerateResponse(response=response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with phi3:mini generation: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting MiniVault API...")
    print("📍 API available at: http://localhost:8000")
    print("📋 API docs at: http://localhost:8000/docs")
    print("📝 Logs written to: logs/log.jsonl")
    print("\n" + "="*50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
