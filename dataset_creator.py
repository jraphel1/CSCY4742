import json
import random
from typing import List, Tuple, Dict, Any

manual_annotations = [
    ("Reconnaissance", "B-TACTIC"),
    ("Gather Victim Host Information: Software", "B-TECHNIQUE"),
    ("Gather Victim Host Information: Hardware", "B-TECHNIQUE"),
    ("Gather Victim Identity Information: Credentials", "B-TECHNIQUE"),
    ("Gather Victim Network Information: IP Addresses", "B-TECHNIQUE"),
    ("Gather Victim Identity Information: Email Addresses", "B-TECHNIQUE"),
    ("Gather Victim Org Information: Business Relationships", "B-TECHNIQUE"),
    ("Resource Development", "B-TACTIC"),
    ("Develop Capabilities: Exploits", "B-TECHNIQUE"),
    ("Acquire Infrastructure: Server", "B-TECHNIQUE"),  # Fixed missing quote
    ("Obtain Capabilities: Tool", "B-TECHNIQUE"),
    ("Obtain Capabilities: Vulnerabilities", "B-TECHNIQUE"),
    ("Develop Capabilities: Malware", "B-TECHNIQUE"),
    ("Obtain Capabilities: Artificial Intelligence", "B-TECHNIQUE"),
    ("Compromise Infrastructure: Network Devices", "B-TECHNIQUE"),
    ("Initial Access", "B-TACTIC"),
    ("Phishing", "B-TECHNIQUE"),
    ("Execution", "B-TACTIC"),
    ("User Execution: Malicious File", "B-TECHNIQUE"),
    ("Command and Scripting Interpreter: PowerShell", "B-TECHNIQUE"),
    ("Command and Scripting Interpreter: Lua", "B-TECHNIQUE"),
    ("Command and Scripting Interpreter: Python", "B-TECHNIQUE"),
    ("Command and Scripting Interpreter: Visual Basic", "B-TECHNIQUE"),
    ("Persistence", "B-TACTIC"),
    ("Create or Modify System Process: Windows Service", "B-TECHNIQUE"),
    ("Server Software Component: Web Shell", "B-TECHNIQUE"),
    ("Privilege Escalation", "B-TACTIC"),
    ("Create or Modify System Process: Windows Service", "B-TECHNIQUE"),
    ("Abuse Elevation Control Mechanism: Sudo and Sudo Caching", "B-TECHNIQUE"),
    ("Process Injection", "B-TECHNIQUE"),
    ("Defense Evasion", "B-TACTIC"),
    ("Abuse Elevation Control Mechanism: Sudo and Sudo Caching", "B-TECHNIQUE"),
    ("Process Injection", "B-TECHNIQUE"),
    ("Rootkit", "B-TECHNIQUE"),
    ("Impersonation", "B-TECHNIQUE"),
    ("Credential Access", "B-TACTIC"),
    ("Input Capture: Credential API Hooking", "B-TECHNIQUE"),
    ("Discovery", "B-TACTIC"),
    ("Account Discovery: Email Account", "B-TECHNIQUE"),
    ("Lateral Movement", "B-TACTIC"),
    ("Remote Services", "B-TECHNIQUE"),
    ("Remote Services: Remote Desktop Protocol", "B-TECHNIQUE"),
    ("Remote Services: VNC", "B-TECHNIQUE"),
    ("Remote Services: SSH", "B-TECHNIQUE"),
    ("Collection", "B-TACTIC"),
    ("Clipboard Data", "B-TECHNIQUE"),
    ("Input Capture: Credential API Hooking", "B-TECHNIQUE"),
    ("Command and Control", "B-TACTIC"),
    ("Proxy", "B-TECHNIQUE"),
    ("Application Layer Protocol: DNS", "B-TECHNIQUE"),
    ("Exfiltration", "B-TACTIC"),
    ("Impact", "B-TACTIC"),
    ("Data Manipulation", "B-TECHNIQUE"),
]

manual_annotations_defend = [
    ("Harden", "B-TACTIC"),
    ("File Encryption", "B-TECHNIQUE"),
    ("Detect", "B-TACTIC"),
    ("System Call Analysis", "B-TECHNIQUE"),
    ("System Daemon Monitoring", "B-TECHNIQUE"),
    ("Scheduled Job Analysis", "B-TECHNIQUE"),
    ("Process Self-Modification Detection", "B-TECHNIQUE"),
    ("Process Spawn Analysis", "B-TECHNIQUE"),
    ("Process Lineage Analysis", "B-TECHNIQUE"),
    ("Dynamic Analysis", "B-TECHNIQUE"),
    ("Emulated File Analysis", "B-TECHNIQUE"),
    ("Network Traffic Community Deviation", "B-TECHNIQUE"),
    ("Per Host Download-Upload Ratio Analysis", "B-TECHNIQUE"),  # Fixed missing quote
    ("Remote Terminal Session Detection", "B-TECHNIQUE"),
    ("Network Traffic Signature Analysis", "B-TECHNIQUE"),
    ("Inbound Session Volume Analysis", "B-TECHNIQUE"),
    ("Client-Server Payload Profiling", "B-TECHNIQUE"),
    ("Protocol Metadata Anomaly Detection", "B-TECHNIQUE"),
    ("Homoglyph Detection", "B-TECHNIQUE"),
    ("Isolate", "B-TACTIC"),
    ("Executable Allowlisting", "B-TECHNIQUE"),
    ("Executable Denylisting", "B-TECHNIQUE"),
    ("System Call Filtering", "B-TECHNIQUE"),  # Fixed missing quote
    ("Hardware-based Process Isolation", "B-TECHNIQUE"),
    ("Kernel-based Process Isolation", "B-TECHNIQUE"),  # Fixed typo in "Process"
    ("Application-based Process Isolation", "B-TECHNIQUE"),
    ("Email Filtering", "B-TECHNIQUE"),
    ("Deceive", "B-TACTIC"),
    ("Decoy File", "B-TECHNIQUE"),
    ("Evict", "B-TACTIC"),
    ("Process Termination", "B-TECHNIQUE"),
    ("Process Suspension", "B-TECHNIQUE"),
    ("Host Shutdown", "B-TECHNIQUE"),
    ("Host Reboot", "B-TECHNIQUE"),
    ("Restore", "B-TACTIC"),
    ("Restore File", "B-TECHNIQUE"),
    ("Restore Email", "B-TECHNIQUE"),
    ("Restore Software", "B-TECHNIQUE"),
]

all_annotations = []
for item in manual_annotations:
    all_annotations.append((item[0], item[1], "OFFENSE"))
for item in manual_annotations_defend:
    all_annotations.append((item[0], item[1], "DEFENSE"))
    
def create_bio_tags(entity_text: str, entity_type: str) -> List[Tuple[str, str]]:
    tokens = entity_text.split()
    bio_tags = []
    
    for i, token in enumerate(tokens):
        if i == 0:
            bio_tags.appens((token, entity_type))
        else:
            i_tag = "I-" + entity_type[2:]
            bio_tags.append((token, i_tag))
            
    return bio_tags

def generate_synthetic_sentences(annotations: List[Tuple[str, str, str]], num_samples: int = 500) -> List[Dict[str, Any]]:
    samples = []
    
    tactics = [ann for ann in annotations if ann[1] == "B-TACTIC"]
    techniques = [ann for ann in annotations if ann[1] == "B-TECHNIQUE"]
    
    for _ in range(num_samples):
        if random.random() < 0.5:
            category = "OFFENSE"
            category_annotations = [a for a in annotations if a[2] == "OFFENSE"]
            category_tactics = [a for a in tactics if a[2] == "OFFENSE"]
            category_techniques = [a for a in techniques if a[2] == "OFFENSE"]
        else:
            category = "DEFENSE"
            category_annotations = [a for a in annotations if a[2] == "DEFENSE"]
            category_tactics = [a for a in tactics if a[2] == "DEFENSE"]
            category_techniques = [a for a in techniques if a[2] == "DEFENSE"]
            
        tactic = random.choice(category_tactics)
        
        num_techniques = random.randint(1, 3)
        selected_techniques = random.sample(category_techniques, min(num_techniques, len(category_techniques)))
        
        if category == "OFFENSE":
            templates = [
                f"The threat actor used the {tactic[0]} tactic along with {' and '.join([t[0] for t in selected_techniques])} to compromise the system.",
                f"Analysis revealed {tactic[0]} activity, specifically {', '.join([t[0] for t in selected_techniques])}.",
                f"The attack involved {tactic[0]}, utilizing {' and '.join([t[0] for t in selected_techniques])}.",
                f"Indicators of {tactic[0]} were detected, including {', '.join([t[0] for t in selected_techniques])}.",
                f"Security logs showed evidence of {tactic[0]} with {' and '.join([t[0] for t in selected_techniques])}."
            ]
        else:
            templates = [
                f"The security team implemented {tactic[0]} measures including {' and '.join([t[0] for t in selected_techniques])}.",
                f"Defense strategy focused on {tactic[0]}, specifically {', '.join([t[0] for t in selected_techniques])}.",
                f"The incident response involved {tactic[0]}, utilizing {' and '.join([t[0] for t in selected_techniques])}.",
                f"Security operations performed {tactic[0]} by deploying {', '.join([t[0] for t in selected_techniques])}.",
                f"Mitigation involved {tactic[0]} through {' and '.join([t[0] for t in selected_techniques])}."
            ]
            
        sentence = random.choice(templates)
        
        tokens_with_tags = []
        for word in sentence.split():
            clean_word = word.rstrip(',.;:')
            
            is_entity = False
            for entity, entity_type, _ in category_annotations:
                if clean_word == entity or (clean_word in entity.split() and len(clean_word) > 3):
                    if clean_word == entity.split()[0]:
                        tokens_with_tags.append((word, entity_type))
                    else:
                        i_tag = "I-" + entity_type[2:]
                        tokens_with_tags.append((word, i_tag))
                    is_entity = True
                    break
            
            if not is_entity:
                tokens_with_tags.append((word, "O"))
                
        sample = {
            "text": sentence,
            "tokens": [token for token, _ in tokens_with_tags],
            "tags": [tag for _, tag in tokens_with_tags],
            "category": category
        }
        
        samples.append(sample)
        
    return samples

def convert_to_ner_format(samples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    ner_samples = []
    
    for sample in samples:
        tokens = sample["tokens"]
        tags = sample["tags"]
        
        ner_sample = {
            "tokens": tokens,
            "tags": tags
        }
        
        ner_samples.append(ner_sample)
        
    return ner_samples

synthetic_samples = generate_synthetic_sentences(all_annotations, num_samples = 500)

ner_dataset = convert_to_ner_format(synthetic_samples)

random.shuffle(ner_dataset)
dataset_size = len(ner_dataset)
train_size = int(0.8 * dataset_size)
val_size = int(0.1 * dataset_size)

train_data = ner_dataset[:train_size]
val_data = ner_dataset[train_size:train_size+val_size]
test_data = ner_dataset[train_size+val_size:]

def save_jsonl(data, filename):
    with open(filename, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')
            
save_jsonl(train_data, 'cybersec_ner_train.jsonl')
save_jsonl(val_data, 'cybersec_ner_val.jsonl')
save_jsonl(test_data, 'cybersec_ner_test.jsonl')

print("Sample entries from the dataset:")
for i in range(min(5, len(train_data))):
    print(f"\nSample {i+1}:")
    print(f"Tokens: {train_data[i]['tokens']}")
    print(f"Tags: {train_data[i]['tags']}")
    print(f"Text: {' '.join(train_data[i]['tokens'])}")
    
def create_prompt_completion_format(samples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    prompt_completion_data = []
    
    for sample in samples:
        tokens = sample["tokens"]
        tags = sample["tags"]
        text = " ".join(tokens)
        
        labeled_entities = []
        current_entity = []
        current_tag = None
        
        for token, tag in zip(tokens, tags):
            if tag.startswith("B-"):
                if current_entity:
                    entity_text = " ".join(current_entity)
                    labeled_entities.append(f"<{current_tag}>{entity_text}</{current_tag}")
                    current_entity = []
                    
                current_entity.append(token)
                current_tag = tag[2:]
                
            elif tag.startswith("I-"):
                current_entity.append(token)
                
            else:
                if current_entity:
                    entity_text = " ".join(current_entity)
                    labeled_entities.append(f"<{current_tag}>{entity_text}</{current_tag}>")
                    current_entity = []
                    
                labeled_entities.append(token)
                
        if current_entity:
            entity_text = " ".join(current_entity)
            labeled_entities.append(f"{current_tag}>{entity_text}</{current_tag}>")
            
        labeled_text = " ".join(labeled_entities)
        
        prompt = f"Identify cybersecurity tactics and techniques in the following text:\n\n{text}"
        completion = labeled_text
        
        prompt_completion_data.append({
            "prompt": prompt,
            "completion": completion
        })
        
    return prompt_completion_data

prompt_completion_data = create_prompt_completion_format(ner_dataset)
save_jsonl(prompt_completion_data[:train_size], 'cybersec_prompt_completion_train.jsonl')
save_jsonl(prompt_completion_data[train_size:train_size+val_size], 'cybersec_prompt_completion_val.jsonl')
save_jsonl(prompt_completion_data[train_size+val_size:], 'cybersec_prompt_completion_test.jsonl')

print("\nCreated datasets in two formats:")
print("1. Standard NER format (tokens and tags)")
print("2. Prompt-completion format for instruction fine-tuning")
print("\nFiles created:")
print("- cybersec_ner_train.jsonl")
print("- cybersec_ner_val.jsonl")
print("- cybersec_ner_test.jsonl")
print("- cybersec_prompt_completion_train.jsonl")
print("- cybersec_prompt_completion_val.jsonl")
print("- cybersec_prompt_completion_test.jsonl")