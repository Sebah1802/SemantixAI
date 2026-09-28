import json
import os

from ai_module.llm_predictor import predict_function_name

from ai_module.confidence_engine import (
    calculate_confidence,
    generate_xai_explanation
)


# ============================================================
# SEMANTIX AI MAIN PIPELINE
# ============================================================

def process_extracted_functions(
    input_json="sample_data/functions.json",
    output_json="sample_data/predictions.json"
):

    """
    SEMANTIX AI complete processing pipeline.

    Stage 1:
        Read Ghidra-extracted function information.

    Stage 2:
        CodeT5 predicts a meaningful function name.

    Stage 3:
        Confidence engine evaluates supporting evidence.

    Stage 4:
        XAI generates a human-readable explanation.

    Stage 5:
        Results are saved to predictions.json.
    """

    print()
    print("=" * 70)
    print("              SEMANTIX AI")
    print("     Reverse Engineering & Function Recovery")
    print("=" * 70)

    # ========================================================
    # INPUT
    # ========================================================

    if not os.path.exists(input_json):

        print(
            f"[ERROR] Input file not found: {input_json}"
        )

        return

    # ========================================================
    # READ GHIRDA OUTPUT
    # ========================================================

    with open(
        input_json,
        "r"
    ) as f:

        functions = json.load(f)

    print()
    print(
        f"[INFO] Processing {len(functions)} function(s)..."
    )

    predictions = []

    # ========================================================
    # PROCESS EACH FUNCTION
    # ========================================================

    for index, fn in enumerate(
        functions,
        start=1
    ):

        function_id = fn.get(
            "id",
            "unknown"
        )

        code = fn.get(
            "decompiled_code",
            ""
        )

        callers = fn.get(
            "callers",
            []
        )

        callees = fn.get(
            "callees",
            []
        )

        # ----------------------------------------------------
        # DISPLAY FUNCTION
        # ----------------------------------------------------

        print()
        print("=" * 70)

        print(
            f"[FUNCTION {index}] {function_id}"
        )

        print("-" * 70)

        print(
            "[INPUT] Decompiled Code:"
        )

        print(code)

        print()

        print(
            "[INPUT] Callers:"
        )

        print(
            ", ".join(callers)
            if callers
            else "None"
        )

        print()

        print(
            "[INPUT] Callees:"
        )

        print(
            ", ".join(callees)
            if callees
            else "None"
        )

        # ----------------------------------------------------
        # MODULE 2
        # CODET5 PREDICTION
        # ----------------------------------------------------

        print()
        print(
            "[MODULE 2] AI Function Name Recovery"
        )

        predicted_name = predict_function_name(
            fn
        )

        # ----------------------------------------------------
        # MODULE 3
        # CONFIDENCE
        # ----------------------------------------------------

        print()
        print(
            "[MODULE 3] Confidence Scoring"
        )

        confidence = calculate_confidence(
            predicted_name,
            code,
            callers,
            callees
        )

        print(
            f"[RESULT] Confidence: {confidence}%"
        )

        # ----------------------------------------------------
        # MODULE 4
        # XAI
        # ----------------------------------------------------

        print()
        print(
            "[MODULE 4] Explainable AI"
        )

        explanation = generate_xai_explanation(
            predicted_name,
            code,
            callers,
            callees
        )

        print(
            "[RESULT] Explanation:"
        )

        print(
            explanation
        )

        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        predictions.append(
            {
                "function_id": function_id,
                "predicted_name": predicted_name,
                "confidence_score": confidence,
                "xai_explanation": explanation,
                "callers": callers,
                "callees": callees
            }
        )

    # ========================================================
    # SAVE OUTPUT
    # ========================================================

    output_directory = os.path.dirname(
        output_json
    )

    if output_directory:

        os.makedirs(
            output_directory,
            exist_ok=True
        )

    with open(
        output_json,
        "w"
    ) as f:

        json.dump(
            predictions,
            f,
            indent=4
        )

    # ========================================================
    # FINAL MESSAGE
    # ========================================================

    print()
    print("=" * 70)

    print(
        "[SUCCESS] SEMANTIX AI processing completed."
    )

    print(
        f"[OUTPUT] {output_json}"
    )

    print("=" * 70)
    print()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    process_extracted_functions()
