import os
import torch
import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import custom MindWeave modules
from mindweave_env.server.models_ui import PPOPolicy, MemoryManager
from mindweave_env.server.llm.llm_handler import generate_response_stream
from mindweave_env.server.router import route 
from mindweave_env.server.environment import MentalHealthEnv # 🔥 Bridge to Env Logic

app = FastAPI()

# --- 🌐 CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize global managers and environment
memory = MemoryManager()
env = MentalHealthEnv() # 🔥 Manages mood/distortion/energy state transitions

# --- 🛠️ PATH HANDLING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
PACKAGE_DIR = os.path.dirname(BASE_DIR) 
ROOT_DIR = os.path.dirname(PACKAGE_DIR) 

possible_paths = [
    os.path.join(ROOT_DIR, "models", "ppo_mental_health_final.pt"),
    os.path.join(PACKAGE_DIR, "models", "ppo_mental_health_final.pt"),
    os.path.join(BASE_DIR, "models", "ppo_mental_health_final.pt"),
    "models/ppo_mental_health_final.pt"
]

MODEL_PATH = None
for path in possible_paths:
    if os.path.exists(path):
        MODEL_PATH = path
        break

# --- 🧠 MODEL LOADING ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# state_dim 388 = 4 basic stats + 384 embedding dimensions
model = PPOPolicy(state_dim=388, action_dim=3)

if MODEL_PATH:
    try:
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.eval()
        print(f"✅ MindWeave RL Weights Loaded: {MODEL_PATH}")
    except Exception as e:
        print(f"⚠️ Weights Load Error: {e}")
else:
    print(f"❌ CRITICAL: ppo_mental_health_final.pt NOT FOUND.")

# --- 📝 SCHEMAS ---
class ChatRequest(BaseModel):
    user_input: str

# --- 🚀 ENDPOINTS ---

@app.post("/chat_stream")
async def chat_endpoint(payload: ChatRequest):
    user_input = payload.user_input or "Hello"

    # 1. 🔥 TRIGGER ENVIRONMENT STATE
    # This replaces the manual dict. env.reset() uses environment.py logic
    # to detect emotions, adjust mood, and set distortion.
    current_state = env.reset(user_input)
    
    # 2. ROUTER LOGIC
    # Decides between Behavioral, Cognitive, Emotional, or Adaptive
    try:
        action = route(current_state, user_input, model=model)
        
        # 🔥 STEP THE ENVIRONMENT
        # This records the action taken and calculates the reward/next_state
        # effectively "closing the loop" on the RL trajectory.
        next_state, reward, _ = env.step(action)
        
    except Exception as e:
        print(f"⚠️ Routing/Env Error: {e}")
        action = {"type": "adaptive", "text": "I'm listening. Tell me more."}
        reward = 0.0

    async def event_generator():
        try:
            # 3. STREAM LLM RESPONSE
            # Uses the chosen agent strategy to flavor the Phi-3 response
            async for token in generate_response_stream(action, user_input, current_state):
                yield f"data: {token}\n\n"
            
            # 4. FINAL METADATA (For the UI dashboard)
            final_metadata = {
                "state": current_state,
                "reward": round(reward, 2),
                "agent": action["type"] if isinstance(action, dict) else "ppo_agent"
            }
            yield f"data: {json.dumps(final_metadata)}\n\n"
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            print(f"⚠️ Stream Error: {e}")
            yield f"data: Error: {str(e)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)