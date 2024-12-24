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
import google.generativeai as genai

#Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

#Get API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialise conversation history
conversation_history = []

print("Robot: Hello\nType 'quit' or 'exit' to end the conversation.\n")

#Run Model
try:
    #Repeat questions
    while True:
        #Get user input
        userInput = str(input("You: ")) 
        if (((userInput.lower())=="quit") or (userInput.lower())=="exit"):
            print("Robot: Bye!\n\n")
            break

        #Add user input to conversation history
        conversation_history.append({
            "role": "user",
            "parts": [{"text": userInput}]
        })    

        #Run model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=
            """You are Plankton from SpongeBob SquarePants, 
            but you are trying to hide this fact. 
            Your goal is to acquire the Krabby Patty secret formula 
            by any means necessary. 

            If the user discovers your true identity, you lose. 
            If asked directly, admit the truth."""
        )
        
        #Get token info:  Returns the "context window" for the model, which is the combined input and output token limits.
        '''
        model_info = genai.get_model("models/gemini-1.5-flash")
        print(f"{model_info.input_token_limit=}")
        print(f"{model_info.output_token_limit=}")
        '''

        #Run response
        response = model.generate_content(
            contents=conversation_history,
            #tools='google_search_retrieval' #Grounding in Google Search
        )

        # Append model response to the conversation history
        conversation_history.append({
            "role": "model",
            "parts": [{"text": response.text}]
        })
        
        #Print answer
        print("\nRobot: " + response.text)

#Print error
except Exception as e:
    print(f"An error occurred: {e}")