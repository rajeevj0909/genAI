from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import google.generativeai as genai

app = Flask(__name__)

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize conversation history and selected role/goal
conversation_history = []
ai_role_goal = None

# Define a list of possible roles and goals for the game
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

role_goal_examples = "\n".join([f"Role: {item['role']} | Goal: {item['goal']}" for item in roles_and_goals])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global ai_role_goal, conversation_history

    try:
        # Generate the role and goal using the model
        gameModel = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                f"You are tasked with selecting a unique role and goal for yourself. "
                f"Please choose a character role and an associated goal. "
                f"Your role and goal should be interesting, creative, and aligned with achieving the goal. "
                f"Here are some examples to inspire you:\n{role_goal_examples}\n"
                f"Choose a marvel character that is a popular and fun from a film, book or TV Show. Be creative! "
                f"Then, state your role and goal in a short format."
            )
        )
        characterInfo = gameModel.generate_content(
            contents=["Generate a role and goal."],
            generation_config={"temperature": 2} #Higher temperature result in more creative character roles and goals
        )
        ai_role_goal = characterInfo.text.strip()
        conversation_history = []  # Reset history
        return jsonify({"message": "Game started! The AI has picked its secret role and goal. Start guessing!"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history, ai_role_goal

    user_input = request.json.get('userInput', '')
    if not user_input:
        return jsonify({"error": "User input is required"}), 400

    conversation_history.append({"role": "user", "parts": [{"text": user_input}]})

    try:
        # After the user input, check if the game is won, lost or still ongoing
        game_status = check_game_status()
    
        system_instruction = (
            f"This is you: {ai_role_goal}."
            f"Keep your identity and goal a secret throughout the game! Use the user to achieve your goal. "
            f"Provide clues throughout the game, but don't reveal too much."
        )

        if game_status == "won":
            system_instruction = (
            f"This is you: {ai_role_goal}."
            f"Keep your identity and goal a secret throughout the game! Use the user to achieve your goal. "
            f"The user has now won the game. Reveal your identity and goal if you have not already. "
            f"Answer any other questions the user may have."
        )
        elif game_status == "lost":
            system_instruction = (
            f"This is you: {ai_role_goal}."
            f"Keep your identity and goal a secret throughout the game! Use the user to achieve your goal. "
            f"The user has given up. Reveal your identity and goal if you have not already. "
            f"Answer any other questions the user may have."
        )

        guessModel = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        gameResponse = guessModel.generate_content(contents=conversation_history)
        conversation_history.append({"role": "model", "parts": [{"text": gameResponse.text}]})
        
        # If game is won or lost, return the status message and update button color
        return jsonify({
            "response": gameResponse.text,
            "gameStatus": game_status,  # "won" or "lost"
            #"buttonColor": "green" if game_status == "won" else "red"
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/start_over', methods=['POST'])
def start_over():
    global ai_role_goal, conversation_history

    # Reset the game to start over
    ai_role_goal = None
    conversation_history = []
    return jsonify({"message": "Game has been reset. Start a new game!"})

def check_game_status():
    try:
        # Use a new model to analyze the conversation and determine the status
        gameStatusModel = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                "You are an AI referee in a guessing game. Analyze the following conversation history "
                "and determine the status of the game. The conversation involves a user interacting with "
                "an AI, and the goal of the game is for the user to guess the AI's secret role and goal. "
                "If the user says 'I give up', the game is lost by the user. If the user says 'I know who you are', "
                "the game is won by the user. If neither of these conditions is met, the game is ongoing. "
                "Analyze the conversation and respond with one of the following: 'won', 'lost', or 'ongoing'."
            )
        )
        
        # Pass the conversation history to the model
        conversation_input = "\n".join([f"{item['role']}: {item['parts'][0]['text']}" for item in conversation_history])
        gameStatusResponse = gameStatusModel.generate_content(contents=[conversation_input])

        # Determine the game status based on the model's response
        game_status = gameStatusResponse.text.strip().lower()

        print(f"Game status: {game_status}")
        return game_status

    except Exception as e:
        return f"An error occurred while determining the game status: {e}"

if __name__ == '__main__':
    app.run(debug=True)
