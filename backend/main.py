from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.orchestrator import build_graph
from backend.db import init_db
from backend.memory import save_memory  

app = FastAPI()
init_db()

# ✅ CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build agent graph
graph = build_graph()


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


@app.post("/generate")
def generate(prompt: str):
    state = {"input": prompt}

    result = graph.invoke(state)
    save_memory(prompt, result.get("final_code", ""))

    final_code = result.get("final_code", "")

    # Detect if it's FastAPI server
    is_server = "FastAPI" in final_code

    return {
        "summary": {
            "task": prompt,
            "status": "success"
        },
        "agents": {
            "planner": result.get("tasks", ""),
            "developer": result.get("code", ""),
            "reviewer": result.get("review", ""),
            "tester": result.get("tests", ""),
            "debugger": final_code
        },
        "execution": {
            "type": "server" if is_server else "script",
            "status": "skipped" if is_server else "executed",
            "message": "Run using: uvicorn main:app --reload" if is_server else result.get("output", ""),
            "error": result.get("error", None)
        }
    }