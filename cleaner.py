import json
import re

input_file = "cybersec_prompt_completion_val.jsonl"
output_file = "cybersec_chat_format_cleaned_val.jsonl"

def fix_tags(text):
    text = re.sub(r'\bTACTIC', r'<TACTIC>', text)
    text = re.sub(r'\bTECHNIQUE', r'<TECHNIQUE>', text)
    text = re.sub(r'(?<!<)/?TACTIC\b', r'</TACTIC>', text)
    text = re.sub(r'(?<!<)/?TECHNIQUE\b', r'</TECHNIQUE>', text)
    text = re.sub(r'<(/)?(TACTIC|TECHNIQUE)[^>]*>', r'<\1\2\>', text)
    
    return text

with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
    for line in fin:
        try:
            data = json.loads(line)
            prompt = data.get("prompt", "").strip()
            completion = data.get("completion", "").strip()
            
            cleaned_completion = fix_tags(completion)
            
            chat_example = {
                "messages": [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": cleaned_completion}
                ]
            }
            
            fout.write(json.dumps(chat_example) + "\n")
        except Exception as e:
            print("Error processing line:", e)

print("Cleaning and conversion complete.")