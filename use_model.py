import openai
import os
import requests
from bs4 import BeautifulSoup

def use_fine_tuned_model(model_id, input_text = None, url = None):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            input_text = soup.get_text(separator = '\n').strip()
            print("Extracted text from URL.")
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return
        
    elif not input_text:
        print("Please provide either text input or a URL.")
        return
    
    try:
        system_prompt = """You are a cybersecurity expert specializing in the MITRE ATT&CK framework. 
                            Your task is to thoroughly analyze text and identify ALL relevant MITRE ATT&CK tactics and techniques present.
                            Be comprehensive - don't miss any techniques mentioned in the text.
                            Always include both the tactic name (e.g., Defense Evasion) and associated techniques."""

        # Few-shot example to guide the model
        few_shot_example = """Example input: 
                                "The malware employs string obfuscation to hide command strings and uses PowerShell scripts to establish persistence through scheduled tasks. It also communicates with C2 servers using encrypted HTTPS traffic."

                                Example output:
                                The cybersecurity tactics and techniques from the MITRE ATT&CK Framework identified in the text are:
                                Tactic: Defense Evasion
                                    - Technique: Obfuscated Files or Information (T1027)
                                    - Technique: Encrypted Channel (T1573)
                                Tactic: Execution
                                    - Technique: PowerShell (T1059.001)
                                Tactic: Persistence
                                    - Technique: Scheduled Task/Job (T1053)
                                Tactic: Command and Control
                                    - Technique: Encrypted Channel (T1573.002)"""

        prompt = f"""Perform a COMPREHENSIVE analysis of the following text. Identify ALL MITRE ATT&CK Tactics and Techniques present - don't miss any!

                Text for analysis:
                {input_text}

                Follow this specific format in your response:
                The cybersecurity tactics and techniques from the MITRE ATT&CK Framework identified in the text are:
                Tactic: [Tactic Name]
                    - Technique: [Technique Name] ([Technique ID if possible])
                    - Technique: [Technique Name] ([Technique ID if possible])
                Tactic: [Tactic Name]
                    - Technique: [Technique Name] ([Technique ID if possible])

                Be as thorough as possible. Identify ALL tactics and techniques mentioned in the text, even subtle ones."""

        response = openai.chat.completions.create(
            model = model_id,
            messages = [
                {"role": "system", "content": "You are a cybersecurity expert specializing in the MITRE ATT&CK Framework. Your task is to identify MITRE ATT&CK tactics and techniques in the text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens = 1500,
            temperature = 0.3
        )
        message_content = response.choices[0].message.content
        print(message_content.strip())
    except Exception as e:
        print(f"Error in model response: {e}")
        
        
def main():
    print("Choose input method:")
    print("1. Input Text")
    print("2. Input URL")
    
    choice = input("Enter input method (1 or 2):\n")
    
    if choice == '1':
        text = input("Enter text for analysis:\n")
        use_fine_tuned_model("ft:gpt-3.5-turbo-0125:personal::BTfUT7KW", input_text = text)
    elif choice == '2':
        url = input("Enter CTI Report URL:\n")
        use_fine_tuned_model("ft:gpt-3.5-turbo-0125:personal::BTfUT7KW", url = url)
    else:
        print("Please choose either 1 or 2")
        
if __name__ == '__main__':
    main()