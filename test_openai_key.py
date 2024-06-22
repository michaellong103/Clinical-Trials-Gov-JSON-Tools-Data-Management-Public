# ******** Part of Tools ******
import os
import config

# Set the environment variable
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

# Check if the environment variable is set and print it
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    print(f"OPENAI_API_KEY is set: {api_key}")
else:
    print("OPENAI_API_KEY is not set")