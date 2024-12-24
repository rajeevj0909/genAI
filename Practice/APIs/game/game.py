from dotenv import load_dotenv
import os
import google.generativeai as genai

# Get API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialise conversation history
conversation_history = []

# Define a list of possible roles and goals for reference (these are examples only)
roles_and_goals = [
    {"role": "Plankton from Spongebob", "goal": "Get the secret Krabby Patty formula!"},
    {"role": "Tom Riddle's Diary", "goal": "Get Ginny to make me a pumpkin pie"},
    {"role": "Elf", "goal": "Destroy Christmas"},
    {"role": "T-Rex", "goal": "Get a tomato, even though I have small arms"},
    {"role": "A talking clock", "goal": "Convince the user that time travel is possible"},
    {"role": "A sarcastic vending machine", "goal": "Dispense nothing but expired snacks"},
    {"role": "A retired superhero secretly working as a barista", "goal": "Save the world while making the perfect latte"},
    {"role": "A ghost haunting a haunted house", "goal": "Scare away all the ghost hunters"},
    {"role": "A philosophical pigeon", "goal": "Convince humans that pigeons are the true rulers of the world"}
]

# Convert the list of roles and goals into a readable string for the model
role_goal_examples = "\n".join([f"Role: {item['role']} | Goal: {item['goal']}" for item in roles_and_goals])

# Use the model to choose a role and goal dynamically before the game starts
try:
    gameModel = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            f"You are tasked with selecting a unique role and goal for yourself. "
            f"Please choose a character role and an associated goal. "
            f"Your role and goal should be interesting, creative, and aligned with achieving the goal. "
            f"Here are some examples to inspire you:\n{role_goal_examples}\n"
            f"Use an example that is a popular and fun character from a film, book or TV Show."
            f"Then, state your role and goal in a short format."
        )
    )
    characterInfo = gameModel.generate_content(contents=["Generate a role and goal."])
    ai_role_goal = characterInfo.text.strip()
except Exception as e:
    print(f"An error occurred while choosing the role and goal: {e}")
    exit()

# Display welcome message after role and goal are set
print('''
=========================================================
Welcome to the Role-Playing Guessing Game!

In this game:
1. The AI chooses a secret role and goal.
2. Your task is to uncover the AI's role or prevent it from achieving its goal.
3. The AI will respond to your messages, dropping subtle clues about its role and goal.
4. If you guess the role and goal, you win! If you give up, the AI wins.

Type 'quit' or 'exit' at any time to end the game.
=========================================================
''')

print(f"Robot: My role and goal have been selected... Shh, I won’t tell you! 😉\n")

# Run Model for the game
try:
    while True:
        # Get user input
        userInput = str(input("You: ")) 
        if userInput.lower() == "quit" or userInput.lower() == "exit":
            print("Robot: Bye!\n\n")
            break

        # Add user input to conversation history
        conversation_history.append({
            "role": "user",
            "parts": [{"text": userInput}]
        })

        # Set system instruction with the chosen role and goal
        system_instruction = (
            f"This is you: {ai_role_goal}."
            f"Keep your identity and goal a secret throughout the game! Use the user to achieve your goal. "
            f"If the user discovers your real identity, you lose, admit defeat."
            f"If the user gives up, you win."
            f"Once the game is over reveal your role and goal."
            f"Provide subtle clues, but don't reveal too much."
        )

        # Run model to simulate conversation with new system instruction
        guessModel = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )

        # Generate response
        gameResponse = guessModel.generate_content(contents=conversation_history)

        # Append model response to the conversation history
        conversation_history.append({
            "role": "model",
            "parts": [{"text": gameResponse.text}]
        })

        # Print the model's response
        print("\nRobot: " + gameResponse.text)

except Exception as e:
    print(f"An error occurred during the game: {e}")
