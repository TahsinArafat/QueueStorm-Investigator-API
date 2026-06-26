import json
import httpx

# Load sample cases
with open("Preliminary Questions and Resources/SUST_Preli_Sample_Cases.json") as f:
    data = json.load(f)

outputs = []

print("Generating official sample outputs...\n")

for case in data["cases"]:
    case_id = case["id"]
    input_data = case["input"]
    
    print(f"Processing {case_id}...")
    
    try:
        response = httpx.post(
            "http://127.0.0.1:8000/analyze-ticket",
            json=input_data,
            timeout=30.0
        )
        
        if response.status_code == 200:
            output = response.json()
            outputs.append({
                "case_id": case_id,
                "label": case["label"],
                "output": output
            })
            print(f"  ✅ Generated")
        else:
            print(f"  ❌ Failed with status {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

# Save to file
with open("queuestorm_sample_outputs.json", "w") as f:
    json.dump(outputs, f, indent=2)

print(f"\n✅ Generated outputs for {len(outputs)}/10 cases")
print("✅ Saved to: queuestorm_sample_outputs.json")

