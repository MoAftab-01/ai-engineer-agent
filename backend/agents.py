from langchain_community.chat_models.ollama import ChatOllama
from backend.tools import run_code

llm = ChatOllama(model="llama3")


# 🧠 Planner Agent
def planner_agent(state):
    tasks = llm.invoke(f"""
    Break this into clear backend development steps:

    {state.get('input', '')}

    Return only steps.
    """).content

    return {**state, "tasks": tasks}


# 👨‍💻 Developer Agent
def developer_agent(state):
    tasks = state.get("tasks", "")

    code = llm.invoke(f"""
    You are an expert backend developer.

    Based on these tasks:
    {tasks}

    Generate FULL working FastAPI code.

    Requirements:
    - Include imports
    - Create FastAPI app
    - Add at least 2 endpoints
    - Return ONLY code (no explanation)
    """).content

    return {**state, "code": code}


# 🔍 Reviewer Agent
def reviewer_agent(state):
    code = state.get("code", "")

    review = llm.invoke(f"""
    You are a strict code reviewer.

    Review this code and list improvements:

    {code}

    Be concise.
    """).content

    return {**state, "review": review}


# 🧪 Tester Agent
def tester_agent(state):
    code = state.get("code", "")

    tests = llm.invoke(f"""
    Write basic test cases for this FastAPI code:

    {code}
    """).content

    return {**state, "tests": tests}


# 🐞 Debugger Agent (SELF-HEALING 🔥)
def debugger_agent(state):
    code = state.get("code", "")
    review = state.get("review", "")

    # Step 1: Execute code
    execution = run_code(code)

    # Step 2: If error → fix it
    if execution.get("error"):
        fix_prompt = f"""
        You are an expert Python debugger.

        Fix this FastAPI code.

        Code:
        {code}

        Error:
        {execution['error']}

        Also consider this review feedback:
        {review}

        Return ONLY corrected working code.
        """

        fixed_code = llm.invoke(fix_prompt).content

        return {
            **state,
            "final_code": fixed_code,
            "error": execution["error"]
        }

    # Step 3: If no error → return as-is
    return {
        **state,
        "final_code": code,
        "output": execution.get("output", "")
    }