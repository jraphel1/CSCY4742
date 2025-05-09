import openai
import os
import json
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
openai.api_key = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------- Load CTI Report --------
def load_report(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# -------- Prompt Engineering --------
def create_prompt(report_text):
    return f"""
You are a cybersecurity analyst.

Read the following cyber threat intelligence (CTI) report and extract all mentioned MITRE ATT&CK techniques.

For each technique, return a JSON object with the following keys:
- "sentence": the sentence where the technique is mentioned
- "technique_id": the MITRE ATT&CK ID (e.g., T1059.001)
- "technique_name": the name (e.g., PowerShell)
- "tactic": the MITRE ATT&CK tactic (e.g., Execution)

If the technique is listed in the D3FEND framework, also include the "d3fend_countermeasures" key with a list of countermeasure IDs (e.g., D3-0037).

Only return valid JSON (an array of these objects).

CTI REPORT:
\"\"\"
{report_text}
\"\"\"
    """

# -------- Call OpenAI GPT-4 --------
def extract_techniques(report_text):
    prompt = create_prompt(report_text)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You extract structured cyber threat intelligence."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        # Try to parse GPT JSON output
        content = response['choices'][0]['message']['content'].strip()
        data = json.loads(content)
        return data
    except Exception as e:
        print("❌ Error parsing GPT output:", e)
        print("🔎 Raw output:", content)
        return []

# -------- Save JSON Output --------
def save_output(data, output_path="annotated_cti_with_d3fend.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Annotations saved to {output_path}")

# -------- Convert to ATT&CK Navigator Format --------
def to_attack_navigator_format(annotations):
    nodes = []
    for annotation in annotations:
        for technique in annotation:
            nodes.append({
                "id": f"attack-pattern--{technique['technique_id']}",
                "type": "attack-pattern",
                "labels": [technique['tactic'], "technique"],
                "name": technique['technique_name'],
                "x_mitre_detection": "TBD",
                "x_mitre_platforms": ["Windows", "Linux", "macOS"],
                "x_mitre_d3fend": technique.get("d3fend_countermeasures", [])
            })
    return {"nodes": nodes}

# -------- Main Program --------
if __name__ == "__main__":
    input_path = "rdp_campaign.txt"  # Replace with your report file
    report = load_report(input_path)
    
    # Extract techniques and countermeasures
    annotations = extract_techniques(report)
    
    # Save output in both formats
    save_output(annotations)
    
    # Convert to ATT&CK Navigator JSON format and save
    navigator_json = to_attack_navigator_format(annotations)
    with open("navigator_output.json", "w", encoding="utf-8") as f:
        json.dump(navigator_json, f, indent=2)
    print(f"✅ Navigator format saved to navigator_output.json")
