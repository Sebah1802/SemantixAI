import re
import torch

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer
)

from ai_module.prompt_generator import generate_semflow_prompt


# ============================================================
# MODEL CONFIGURATION
# ============================================================

MODEL_PATH = "./models/semantix_codet5"

print("[INFO] Loading fine-tuned SEMANTIX CodeT5 model...")
print(f"[INFO] Model path: {MODEL_PATH}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_PATH
)

model.eval()

print("[SUCCESS] Fine-tuned CodeT5 loaded successfully.")


# ============================================================
# CODET5 PREDICTION
# ============================================================

def predict_function_name(func_data):
    """
    Uses CodeT5 to predict the meaningful function name.

    IMPORTANT:
    This function does NOT calculate confidence
    and does NOT generate XAI.

    CodeT5 is responsible only for function-name prediction.
    """

    # --------------------------------------------------------
    # Create semantic prompt
    # --------------------------------------------------------

    prompt = generate_semflow_prompt(func_data)

    print()
    print("-" * 60)
    print("[DEBUG] SEMANTIX INPUT")
    print("-" * 60)
    print(prompt)

    # --------------------------------------------------------
    # Tokenize prompt
    # --------------------------------------------------------

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    # --------------------------------------------------------
    # Run CodeT5
    # --------------------------------------------------------

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_length=32,
            num_beams=5,
            num_return_sequences=1,
            early_stopping=True
        )

    # --------------------------------------------------------
    # Decode model output
    # --------------------------------------------------------

    raw_prediction = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    print("[DEBUG] CodeT5 raw prediction:")
    print(raw_prediction)

    # --------------------------------------------------------
    # Clean prediction with contextual fallback
    # --------------------------------------------------------

    obfuscated_id = func_data.get("obfuscated_name", "")

    clean_name = clean_prediction(
        raw_prediction,
        obfuscated_id=obfuscated_id,
        callees=func_data.get("callees", [])
    )

    print(
        f"[INFO] CodeT5 predicted: {clean_name}"
    )

    return clean_name


# ============================================================
# CLEAN MODEL OUTPUT
# ============================================================

def clean_prediction(raw_prediction, obfuscated_id="", callees=None):
    """
    Converts CodeT5 output into a clean function name.
    Falls back to a domain-driven name if CodeT5 echoes an obfuscated header.
    """

    if callees is None:
        callees = []

    name = raw_prediction.strip().lower()

    # Replace spaces and hyphens
    name = re.sub(
        r"[\s\-]+",
        "_",
        name
    )

    # Keep only valid identifier characters
    name = re.sub(
        r"[^a-zA-Z0-9_]",
        "",
        name
    )

    # Remove repeated underscores
    name = re.sub(
        r"_+",
        "_",
        name
    )

    name = name.strip("_")

    # --------------------------------------------------------
    # GUARDRAIL: Prevent self-echoing obfuscated headers
    # --------------------------------------------------------

    is_obfuscated_echo = (
        name.startswith("sub_")
        or name.startswith("fun_")
        or (obfuscated_id and name == obfuscated_id.lower())
    )

    if is_obfuscated_echo or not name:
        lower_callees = [c.lower() for c in callees]

        if any(api in lower_callees for api in ["strcmp", "strncmp", "memcmp"]):
            return "validate_token_credentials"
        elif any(api in lower_callees for api in ["malloc", "calloc", "memset"]):
            return "allocate_and_initialize_buffer"
        elif any(api in lower_callees for api in ["socket", "connect", "send", "recv"]):
            return "network_socket_handler"
        else:
            return "process_data_buffer"

    return name