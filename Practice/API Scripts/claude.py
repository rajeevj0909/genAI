import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

try:
    # Initialize the Anthropic client
    client = Anthropic(api_key=api_key)

    # Define the prompt
    user_message = "What is the capital of France?"

    # Generate a response from the model
    response = client.messages.create(
        max_tokens=100,  # Specify the maximum number of tokens in the response
        model="claude-3-5-haiku-latest",  # Specify the desired model
        messages=[
            {"role": "user", "content": user_message}  # User input to the model
        ]
    )

    # Extract and print the response text
    print(response['content'])

except Exception as e:
    print(f"An error occurred: {e}")
