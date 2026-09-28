def predict_function_name(function):
    code = function["decompiled_code"].lower()

    if "strcmp" in code and "password" in code:
        return {
            "predicted_name": "check_password",
            "explanation": "The function compares a password with an input value.",
            "confidence": 90
        }

    elif "aes_encrypt" in code:
        return {
            "predicted_name": "encrypt_password",
            "explanation": "The function performs AES encryption on password data.",
            "confidence": 95
        }

    else:
        return {
            "predicted_name": "unknown_function",
            "explanation": "Not enough information to determine the function name.",
            "confidence": 40
        }


# Test function
if __name__ == "__main__":

    test_function = {
        "function_id": "sub_401200",
        "decompiled_code": "int sub_401200(){ return strcmp(password,input); }",
        "callers": ["login"],
        "callees": ["strcmp"]
    }

    result = predict_function_name(test_function)

    print(result)