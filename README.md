🧠 MindWeave: RL-Powered Mental Health Agent System
🚀 Overview

MindWeave is a state-aware mental health support system built using a reinforcement learning (PPO-based) decision engine combined with a multi-agent architecture.

It processes user input through a structured pipeline of:

Emotion Classification
Intent Detection
Agent Selection

Based on internal psychological state variables:

Mood
Energy
Distortion
Sentiment

Each step updates the environment state and produces a reward, enabling adaptive and context-aware responses.

---

🧩 Key Features
🧠 Environment-driven reasoning (state-based decisions)
🎯 Multi-step task pipeline (3 tasks per input)
🔁 9-step evaluation episodes (3 inputs × 3 tasks)
🤖 Multi-agent system:
Emotional
Cognitive
Behavioral
Adaptive
⚡ OpenEnv-compatible inference output ([START] → [STEP] → [END])
💬 Optional real-time chat UI
🧠 Optional local LLM support via Ollama
📊 Achieves ~0.9+ therapeutic score (competitive with LLM baselines)

---

⚙️ System Flow

User Input
↓
Environment State Update
↓
Emotion → Intent → Agent
↓
Policy Decision (RL / Environment)
↓
LLM (Echo only, no reasoning)
↓
Environment Step + Reward

---

🧪 Example Output
[START]
[STEP] step=1 ...
...
[STEP] step=9 ...
[END]

---

🛠️ Setup & Installation
✅ Prerequisites
Python 3.10+
Git

1. Clone Repository
   git clone https://github.com/<your-username>/mindweave-v1.git
   cd mindweave-v1
2. Create Virtual Environment
   python -m venv .venv
   Activate:

Windows

.venv\Scripts\activate

Mac/Linux

source .venv/bin/activate

3. Install Dependencies
   pip install -r requirements.txt

---

🚀 Running the System
▶️ Run Server (OpenEnv)
Recommended:
python -m uv run server
Alternative:
uv run server
Fallback (always works):
python -m uvicorn mindweave_env.server.app:app
🧪 Run Inference (Evaluation)
python -m uv run python inference.py

Expected Output:

[START]
[STEP] ...
[END]

💻 Live UI (Optional)

1. Start UI Backend
   python -m uv run uvicorn mindweave_env.server.main_ui:app --reload
2. Open Frontend

Open:

mindweave_env/index.html

Or run via Live Server:

http://127.0.0.1:5500/mindweave_env/index.html

🤖 Local LLM (Optional)

Install Ollama and run:

ollama pull phi3

Used for chat UI only — not required for evaluation

---

📊 Evaluation

Run:

python -m uv run python -m mindweave_env.server.evaluation.compare_outputs

Results stored in:

mindweave_env/server/evaluation/results/
🧠 Architecture
PPO-based decision policy
Environment-driven state transitions
Multi-agent response system
LLM used only as a response renderer (no reasoning)

---

⚠️ Notes

If uv is not recognized, use:

python -m uv run ...
Ensure commands are run from project root
No GPU required

---

👩‍💻 Author

Akanksha Panda

Built for Meta PyTorch OpenEnv Hackathon
