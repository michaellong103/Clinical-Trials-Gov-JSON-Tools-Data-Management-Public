import json
import os
from openai import OpenAI
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load your OpenAI API key from an environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def load_cleaned_data(cleaned_data_dir):
    clinical_trials = []
    for subdir, _, files in os.walk(cleaned_data_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file.endswith('.json'):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    clinical_trials.extend(data)
    return clinical_trials

def find_clinical_trials(query, clinical_trials):
    # Simple keyword matching
    matching_trials = [trial for trial in clinical_trials if query.lower() in json.dumps(trial).lower()]
    return matching_trials

def generate_response(query, clinical_trials):
    matching_trials = find_clinical_trials(query, clinical_trials)

    if not matching_trials:
        return "Sorry, no clinical trials found matching your query."

    # Prepare a summary of matching trials
    summary = "\n".join([f"Title: {trial['BriefTitle']}\nSummary: {trial['BriefSummary']}\n" for trial in matching_trials[:3]])

    # Use the ChatCompletion API for a better response
    prompt = f"User query: {query}\n\nFound the following clinical trials:\n{summary}\n\nProvide a helpful response to the user."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    # Print the entire response for debugging
    print(response)

    # Correctly access the content of the message
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    cleaned_data_dir = 'data/cleaned'
    clinical_trials = load_cleaned_data(cleaned_data_dir)
    
    print("Welcome to the Clinical Trials Finder!")
    print("You can ask me about clinical trials for various conditions.")
    print("Type 'exit' to end the conversation.")
    
    while True:
        query = input("\nYou: ")
        if query.lower() == 'exit':
            print("Goodbye!")
            break
        
        response = generate_response(query, clinical_trials)
        print(f"\nGPT: {response}")
