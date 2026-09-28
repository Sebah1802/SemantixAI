from ai_module.confidence_engine import (
    calculate_confidence,
    generate_xai_explanation,
)

# Test Scenario: A buffer allocation & clear function
predicted_name = "init_buffer"
decompiled_code = """
void* create_buf(size_t size) {
    void* ptr = malloc(size);
    if (ptr) memset(ptr, 0, size);
    return ptr;
}
"""
callers = ["main", "setup_session"]
callees = ["malloc", "memset"]

confidence = calculate_confidence(
    predicted_name=predicted_name,
    decompiled_code=decompiled_code,
    callers=callers,
    callees=callees,
)

explanation = generate_xai_explanation(
    predicted_name=predicted_name,
    decompiled_code=decompiled_code,
    callers=callers,
    callees=callees,
)

print(f"Predicted Name: {predicted_name}")
print(f"Confidence Score: {confidence}%")
print(f"XAI Explanation: {explanation}")