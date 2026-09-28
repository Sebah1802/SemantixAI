def calculate_confidence(
    predicted_name,
    decompiled_code,
    callers,
    callees
):
    """
    Calculates a system-generated reliability score.

    IMPORTANT:
    This is NOT the probability produced by CodeT5.

    The score represents how strongly the available
    evidence supports the predicted function name.
    """

    score = 50.0

    code = decompiled_code.lower()

    name = predicted_name.lower()

    lower_callees = [
        c.lower()
        for c in callees
    ]

    # ========================================================
    # AVAILABLE EVIDENCE
    # ========================================================

    if code.strip():
        score += 10

    if callers:
        score += 5

    if callees:
        score += 5

    # ========================================================
    # STRING BEHAVIOR
    # ========================================================

    string_apis = [
        "strcmp",
        "strncmp",
        "memcmp",
        "streq"
    ]

    string_words = [
        "compare",
        "check",
        "verify",
        "validate",
        "credential",
        "password",
        "string"
    ]

    if any(
        api in lower_callees
        for api in string_apis
    ):

        if any(
            word in name
            for word in string_words
        ):
            score += 20

    # ========================================================
    # MEMORY BEHAVIOR
    # ========================================================

    memory_apis = [
        "malloc",
        "calloc",
        "realloc",
        "memset"
    ]

    memory_words = [
        "memory",
        "buffer",
        "allocate",
        "initialize",
        "init"
    ]

    if any(
        api in lower_callees
        for api in memory_apis
    ):

        if any(
            word in name
            for word in memory_words
        ):
            score += 20

    # ========================================================
    # NETWORK BEHAVIOR
    # ========================================================

    network_apis = [
        "socket",
        "connect",
        "send",
        "recv"
    ]

    network_words = [
        "network",
        "socket",
        "connect",
        "send",
        "receive",
        "communication"
    ]

    if any(
        api in lower_callees
        for api in network_apis
    ):

        if any(
            word in name
            for word in network_words
        ):
            score += 20

    # ========================================================
    # CODE SEMANTIC EVIDENCE
    # ========================================================

    if "strcmp" in code or "strncmp" in code:

        if any(
            word in name
            for word in [
                "verify",
                "validate",
                "check",
                "compare",
                "credential",
                "password"
            ]
        ):
            score += 10

    if "malloc" in code:

        if any(
            word in name
            for word in [
                "allocate",
                "memory",
                "buffer"
            ]
        ):
            score += 10

    # ========================================================
    # LIMIT SCORE
    # ========================================================

    return min(
        round(score, 1),
        100.0
    )


# ============================================================
# XAI EXPLANATION
# ============================================================

def generate_xai_explanation(
    predicted_name,
    decompiled_code,
    callers,
    callees
):
    """
    Generates a human-readable explanation using
    evidence actually observed in the function.
    """

    code = decompiled_code.lower()

    lower_callees = [
        c.lower()
        for c in callees
    ]

    evidence = []

    # ========================================================
    # STRING EVIDENCE
    # ========================================================

    string_apis = [
        api
        for api in lower_callees
        if api in [
            "strcmp",
            "strncmp",
            "memcmp",
            "streq"
        ]
    ]

    if string_apis:

        evidence.append(
            "string comparison operations such as "
            + ", ".join(string_apis)
        )

    # ========================================================
    # MEMORY EVIDENCE
    # ========================================================

    memory_apis = [
        api
        for api in lower_callees
        if api in [
            "malloc",
            "calloc",
            "realloc",
            "memset"
        ]
    ]

    if memory_apis:

        evidence.append(
            "memory operations such as "
            + ", ".join(memory_apis)
        )

    # ========================================================
    # NETWORK EVIDENCE
    # ========================================================

    network_apis = [
        api
        for api in lower_callees
        if api in [
            "socket",
            "connect",
            "send",
            "recv"
        ]
    ]

    if network_apis:

        evidence.append(
            "network operations such as "
            + ", ".join(network_apis)
        )

    # ========================================================
    # CODE BEHAVIOR
    # ========================================================

    if (
        "strcmp" in code
        or "strncmp" in code
        or "memcmp" in code
    ):

        evidence.append(
            "the code performs a comparison between values"
        )

    if (
        "malloc" in code
        or "calloc" in code
        or "realloc" in code
    ):

        evidence.append(
            "the code dynamically allocates memory"
        )

    if "memset" in code:

        evidence.append(
            "the allocated memory is initialized or cleared"
        )

    # ========================================================
    # CALLER INFORMATION
    # ========================================================

    if callers:

        evidence.append(
            f"the function has {len(callers)} caller function(s)"
        )

    # ========================================================
    # FINAL EXPLANATION
    # ========================================================

    if evidence:

        explanation = (
            f"The predicted function name is "
            f"'{predicted_name}'. "
            f"The analysis observed "
            f"{', '.join(evidence)}. "
            f"These behavioral signals support the predicted "
            f"function purpose."
        )

    else:

        explanation = (
            f"The predicted function name is "
            f"'{predicted_name}'. "
            f"No strong API-level signals were available, "
            f"so the prediction mainly relies on the "
            f"decompiled code structure and semantic context."
        )

    return explanation
