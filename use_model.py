import openai
import os
import requests
from bs4 import BeautifulSoup

class ConversationalAnalyzer:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_id = "ft:gpt-3.5-turbo-0125:personal::BTfUT7KW"
        self.conversation_history = []
        self.last_analysis_text = ""
        self.last_analysis_result = ""
        
    def add_to_history(self, role, content):
        self.conversation_history.append({"role": role, "content": content})
        
    def extract_text_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text(separator='\n').strip()
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None
            
    def analyze_text(self, input_text):
        self.last_analysis_text = input_text
        
        system_prompt = """You are a cybersecurity expert specializing in the MITRE ATT&CK framework. 
                        Your task is to thoroughly analyze text and identify ALL relevant MITRE ATT&CK tactics and techniques present.
                        Be comprehensive - don't miss any techniques mentioned in the text.
                        Always include both the tactic name (e.g., Defense Evasion) and associated techniques."""
        
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

                Be as thorough as possible. Identify ALL tactics and techniques mentioned in the text, even subtle ones.
                
                Additionally, provide MITRE D3FEND recommendations, using the MITRE D3FEND Framework
                
                Identify ALL MITRE D3FEND Tactics and Techniques present
                Follow this specific format in your response:
                Defensive recommendations from the MITRE D3FEND Framework:
                Tactic: [Tactic Name]
                    - Technique: [Technique Name] ([Technique ID if possible])
                Tactic: [Tactic Name]
                    - Technique: [Technique Name] ([Technique ID if possible])"""
        
        try:
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": prompt})
            
            response = self.openai_client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                max_tokens=1500,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            
            # Only update conversation history if this is a new analysis
            if not self.last_analysis_result or input_text.startswith(self.last_analysis_text):
                self.last_analysis_result = result
                self.add_to_history("user", prompt)
                self.add_to_history("assistant", result)
            
            return result
            
        except Exception as e:
            return f"Error in model response: {e}"
            
    def process_input(self, user_input):
        if user_input.lower() in ["exit", "quit", "bye"]:
            return "Exiting conversation. Goodbye!"
            
        if user_input.lower().startswith("http"):
            # Treat as URL
            print("Extracting text from URL...")
            extracted_text = self.extract_text_from_url(user_input)
            if extracted_text:
                print("Text extracted. Analyzing...")
                return self.analyze_text(extracted_text)
            else:
                return "Failed to extract text from the URL. Please try a different URL or paste text directly."
                
        elif user_input.lower().startswith("help"):
            return """
                    Available commands:
                    - Type 'analyze: [your text]' to analyze specific text
                    - Type 'url: [your url]' to analyze content from a URL
                    - Ask follow-up questions about the previous analysis
                    - Type 'history' to see conversation history
                    - Type 'clear' to clear conversation history
                    - Type 'exit', 'quit', or 'bye' to end the conversation
                    """
        elif user_input.lower() == "history":
            if not self.conversation_history:
                return "No conversation history yet."
            
            history = "Conversation History:\n"
            for i, msg in enumerate(self.conversation_history):
                if i % 2 == 0 and msg["role"] == "user":
                    # Only show user prompts, not the technical prompts
                    history += f"User: {msg['content'][:50]}...\n"
            return history
            
        elif user_input.lower() == "clear":
            self.conversation_history = []
            self.last_analysis_text = ""
            self.last_analysis_result = ""
            return "Conversation history cleared."
            
        # Check if this is an analysis request
        elif user_input.lower().startswith("analyze:"):
            text_to_analyze = user_input[8:].strip()  # Remove "analyze:" prefix
            if text_to_analyze:
                print("Analyzing text...")
                return self.analyze_text(text_to_analyze)
            else:
                return "Please provide text to analyze after 'analyze:'"
                
        elif user_input.lower().startswith("url:"):
            url_to_analyze = user_input[4:].strip()  # Remove "url:" prefix
            if url_to_analyze:
                print("Extracting and analyzing from URL...")
                extracted_text = self.extract_text_from_url(url_to_analyze)
                if extracted_text:
                    return self.analyze_text(extracted_text)
                else:
                    return "Failed to extract text from the URL. Please try a different URL."
            else:
                return "Please provide a URL after 'url:'"
            
        else:
            # This is likely a question about previous analysis
            if not self.last_analysis_result:
                return "I don't have any previous analysis to answer questions about. Please use 'analyze:' followed by text to analyze, or 'url:' followed by a URL."
            
            # Handle the question about previous analysis
            try:
                system_prompt = """You are a cybersecurity expert specializing in the MITRE ATT&CK framework.
                                Answer questions about the previous analysis in a conversational manner."""
                
                prompt = f"""Based on this previous MITRE ATT&CK analysis:
                {self.last_analysis_result}
                
                Answer this question conversationally:
                {user_input}"""
                
                response = self.openai_client.chat.completions.create(
                    model=self.model_id,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1500,
                    temperature=0.3
                )
                
                answer = response.choices[0].message.content.strip()
                self.add_to_history("user", user_input)
                self.add_to_history("assistant", answer)
                return answer
                
            except Exception as e:
                return f"Error processing your question: {e}"

def main():
    print("=" * 60)
    print("Welcome to the Conversational MITRE ATT&CK Analysis Tool!")
    print("Type 'analyze: [your text]' to analyze for MITRE ATT&CK techniques")
    print("Type 'url: [your url]' to analyze content from a webpage")
    print("After analysis, you can ask follow-up questions conversationally")
    print("Type 'help' for all commands or 'exit' to quit")
    print("=" * 60)
    
    analyzer = ConversationalAnalyzer()
    
    while True:
        if analyzer.last_analysis_result:
            user_input = input("\nAsk a question about the analysis (or type a command)\n> ")
        else:
            user_input = input("\nWhat would you like to do? (type 'help' for commands)\n> ")
        
        result = analyzer.process_input(user_input)
        
        if result == "Exiting conversation. Goodbye!":
            print(result)
            break
            
        print("\n" + "=" * 60)
        print(result)
        print("=" * 60)

if __name__ == '__main__':
    main()