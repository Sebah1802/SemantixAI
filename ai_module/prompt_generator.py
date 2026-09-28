def generate_semflow_prompt(func_data):
    """
    Creates the semantic context given to CodeT5.

    The original function name is intentionally NOT included
    because the objective is to recover a meaningful name.
    """

    decompiled = func_data.get("decompiled_code", "")
    callers = func_data.get("callers", [])
    callees = func_data.get("callees", [])

    caller_text = ", ".join(callers) if callers else "None"
    callee_text = ", ".join(callees) if callees else "None"

    prompt = f"""
Recover the meaningful function name.

Decompiled code:
{decompiled}

Called functions:
{callee_text}

Callers:
{caller_text}

Function name:
"""

    return prompt.strip()
