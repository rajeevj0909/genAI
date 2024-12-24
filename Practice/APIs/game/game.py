"""
This Python script implements a simple text-based role-playing game using the Gemini API. 

**Gameplay:**

1. You choose a character role and a goal for that character.
2. You interact with the AI by typing messages.
3. The AI responds as the character it was assigned, attempting to achieve its own goal while keeping its true identity a secret. 

**Objective:**

Your goal is to uncover the AI's true identity or prevent it from achieving its goal. 

**How to Play:**

- Type your messages and press Enter.
- Type "quit" or "exit" to end the game.

Enjoy the game!
"""

from dotenv import load_dotenv
import os
import google.generativeai as genai

#Get API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialise conversation history
conversation_history = []
#Player 1 chooses role and goal
print("Welcome to the game!\nChoose a character role and a goal for that character before passing the game to player 2\n")
roleChoice=str(input("What character would you like to be?\n"))
goalChoice=str(input("What goal is the character trying to reach?\n"))
os.system('cls')#Clears terminal to start game for player 2
print("\nRobot: Hello\nType 'quit' or 'exit' to end the conversation.\n")

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
            """You are """ + roleChoice + """. 
            Your goal is by any means necessary to 
            keep your true identity and goal a secret, 
            the goal is to use the user to help you to
            """ + goalChoice + """.
            If the user discovers your true identity, you lose. 
            If you lose, admit the truth."""
        )

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