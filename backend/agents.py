from langchain_groq import ChatGroq

# Initialize LLM safely
def get_llm():
    try:
        return ChatGroq(
            model="llama3-8b-8192",
            temperature=0
        )
    except Exception as e:
        print("LLM init failed:", e)
        return None


def planner_agent(state):
    llm = get_llm()
    if not llm:
        return {**state, "plan": "LLM not available"}

    prompt = f"Create a step-by-step plan for: {state['input']}"
    response = llm.invoke(prompt)

    return {**state, "plan": response.content}