import json

# Load JSON file
with open("../sample_data/functions.json", "r") as file:
    functions = json.load(file)

print("=" * 50)
print("FUNCTIONS LOADED")
print("=" * 50)

for function in functions:
    print(f"\nFunction ID      : {function['function_id']}")
    print(f"Code             : {function['decompiled_code']}")
    print(f"Callers          : {', '.join(function['callers'])}")
    print(f"Callees          : {', '.join(function['callees'])}")

print("\nDone!")