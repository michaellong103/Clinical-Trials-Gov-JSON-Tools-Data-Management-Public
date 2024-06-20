

import openai
from openai import OpenAIError
 
# Set your OpenAI API key
openai.api_key = ''

def generate_embedding(text):
    try:
        # Create an embedding using the new API method
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response['data'][0]['embedding']
        return embedding
    except OpenAIError as e:
        print(f"Error generating embedding for text: {text}")
        print(e)
        return None

# Example usage
if __name__ == "__main__":
    text = "Translate the following text into French: Hello, how are you?"
    embedding = generate_embedding(text)
    if embedding:
        print("Embedding generated successfully!")
    else:
        print("Failed to generate embedding.")
