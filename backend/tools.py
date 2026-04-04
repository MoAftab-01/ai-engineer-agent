import subprocess
import tempfile
import re


def clean_code(code: str):
    code = re.sub(r"```python", "", code)
    code = re.sub(r"```", "", code)

    lines = code.split("\n")
    cleaned = []

    for line in lines:
        if line.strip().startswith(("Here is", "This is", "Explanation")):
            continue
        cleaned.append(line)

    return "\n".join(cleaned)


def is_server_code(code: str):
    return "FastAPI" in code or "app = FastAPI" in code


def run_code(code: str):
    try:
        code = clean_code(code)

        # 🔥 Detect server-type code
        if is_server_code(code):
            return {
                "output": "Detected FastAPI app (server code not executed)",
                "error": None
            }

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
            f.write(code)
            file_name = f.name

        result = subprocess.run(
            ["python", file_name],
            capture_output=True,
            text=True,
            timeout=5
        )

        return {
            "output": result.stdout,
            "error": result.stderr
        }

    except Exception as e:
        return {"error": str(e)}