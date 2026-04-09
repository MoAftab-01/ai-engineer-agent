from fastapi import FastAPI
from backend.agents import planner_agent

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Backend is working 🚀"}


@app.get("/test")
def test():
    return {"status": "ok"}


@app.get("/agent")
def run_agent():
    try:
        state = {"input": "Build a todo app"}
        result = planner_agent(state)
        return result
    except Exception as e:
        return {"error": str(e)}