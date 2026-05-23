"""
This Python script demonstrates a simple conversational AI using the Gemini API. 
Key Features:
- Loads API key from an environment variable (.env file).
- Suppresses unnecessary log messages for a cleaner output.
- Allows for user input and provides responses from the Gemini model.
- Includes basic error handling.
- Maintains a simple conversation history to provide context to the model.
"""

from dotenv import load_dotenv
import os
from google import genai

#Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

#Get API key from .env file
load_dotenv()

# Initialize the new unified GenAI Client
client = genai.Client()

print("Robot: Hello\nType 'quit' or 'exit' to end the conversation.\n")

#Run Model
try:
    # Initialize chat session (automatically manages history/context)
    chat = client.chats.create(model="gemini-2.5-flash")

    #Repeat questions
    while True:
        #Get user input
        userInput = input("You: ").strip() 
        if userInput.lower() in ("quit", "exit"):
            print("Robot: Bye!\n\n")
            break

        if not userInput:
            continue

        #Run response
        response = chat.send_message(userInput)
        
        #Print answer
        print("\nRobot: " + response.text)

#Print error
except Exception as e:
    print(f"An error occurred: {e}")