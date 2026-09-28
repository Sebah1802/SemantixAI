from ai_module.llm_predictor import predict_function_name

sample_func_data = {
    "obfuscated_name": "func_a1",
    "parameters": ["a", "b"],
    "operations": ["ADD"],
    "return_type": "int",
    "constants": [],
    "api_calls": []
}

predicted_name = predict_function_name(sample_func_data)
print(f"\nFinal Cleaned Function Name: {predicted_name}")