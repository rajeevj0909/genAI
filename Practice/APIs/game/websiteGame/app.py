from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Function to get API key from .env file
def get_api_key_from_env():
    load_dotenv()
    return os.getenv("GEMINI_GAME_API_KEY")

# Function to get API key from Google Cloud Secret Manager
def get_api_key_from_secret_manager():
    from google.cloud import secretmanager
    gcloud_project_id = "GCLOUD_PROJECT_ID"  # Replace with GCP project ID for deployment
    #load_dotenv() # Load from .env file for local testing
    #gcloud_project_id = os.getenv("GCLOUD_PROJECT_ID")  # Load from .env file for local testing
    secret_name = f"projects/{gcloud_project_id}/secrets/GEMINI_GAME_API_KEY/versions/latest"
    try:
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(name=secret_name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        return f"An error occurred while accessing the secret: {e}"

app = Flask(__name__)

# Choose which function to use for getting the API key
DEPLOY_TO_CLOUD = False  # Set to True to use Google Cloud Secret Manager, False to use .env file locally
if DEPLOY_TO_CLOUD:
    GEMINI_API_KEY = get_api_key_from_secret_manager()
else:
    GEMINI_API_KEY = get_api_key_from_env()
genai.configure(api_key=GEMINI_API_KEY)

# Initialize conversation history and selected role
conversation_history = []
ai_role = None
game_over = False  # Add this flag to track if the game is over

# Define a list of possible roles for the game
roles = [
    "Plankton from Spongebob",
    "Tom Riddle's Diary",
    "Elf",
    "T-Rex",
    "A talking clock",
    "A sarcastic vending machine",
    "A retired superhero secretly working as a barista",
    "A ghost haunting a haunted house",
    "A philosophical pigeon"
]

role_examples = "\n".join([f"Role: {role}" for role in roles])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global ai_role, conversation_history, game_over

    try:
        character_type = request.json.get('characterType', 'kids')
        # Generate the role using the model
        gameModel = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                f'''You are tasked with selecting a unique role for yourself. 
                Please choose a character role. 
                Your role should be interesting, creative, and fun. 
                Here are some examples to inspire you:
                ''' + role_examples + '''
                Choose a ''' + character_type + ''' character that is popular and fun
                from a film, book or TV Show. It needs to be well-known and identifiable. 
                Be creative! Then, state your role in a short format.'''
            )
        )
        
        characterInfo = gameModel.generate_content(
            contents=["Generate a role."],
            generation_config={"temperature": 1.2} #Higher temperature result in more creative character roles
        )
        ai_role = characterInfo.text.strip()
        game_over = False  # Reset the game_over flag
        conversation_history = []  # Reset history
        return jsonify({"message": "Game started! The AI has picked its secret role. Start guessing!"})
    except Exception as e:
        return jsonify({"error": f"An error occurred creating a character: {e}"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history, ai_role, game_over

    user_input = request.json.get('userInput', '')
    if not user_input:
        return jsonify({"error": "User input is required"}), 400

    conversation_history.append({"role": "user", "parts": [{"text": user_input}]})

    try:
        # After the user input, check if the game is won, lost or still ongoing
        if not game_over:  # Only check game status if the game is not over
            game_status = check_game_status()
        else:
            game_status = "ongoing"  # Keep the game status as ongoing if the game is over

        system_instruction = (
            f'''This is you: {ai_role}.
            Keep your identity a secret throughout the game! Help the user figure out who the character is by providing clues. 
            Provide clues throughout the game, but don't reveal too much.
            When the user asks a question, give a straightforward answer/clue.
            '''
        )

        if game_status == "won" and not game_over:
            game_over = True  # Set the game_over flag to True
            system_instruction = (
                f'''This is you: {ai_role}.
                The user has won the game! Reveal your identity if you have not already.
                Explain yourself and your role to the user.
                Answer any other questions the user may have.
                '''
            )
        elif game_status == "lost" and not game_over:
            game_over = True  # Set the game_over flag to True
            system_instruction = (
                f'''This is you: {ai_role}.
                The user has given up! Reveal your identity if you have not already.
                Explain yourself and your role to the user.
                Answer any other questions the user may have.
                '''
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
            "gameStatus": game_status,  # "won" or "lost" or "ongoing"
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred with the response: {e}"}), 500

def check_game_status():
    try:
        # Use a new model to analyze the conversation and determine the status
        gameStatusModel = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction = f'''
            You are an AI referee in a guessing game. Analyze the following conversation history 
            and determine the status of the game. The conversation involves a user interacting with 
            an AI, and the goal of the game is for the user to guess the character name. 
            If the user says "I give up" or something like this, the game is lost by the user. 
            The AI has a secret role that must keep hidden from the user, here is the role:
            {ai_role} 
            If the user says the name of the character or identifies the character correctly, 
            the game is won by the user. If neither of these conditions are met, or the user has 
            guessed the incorrect character, the game is ongoing. Analyse the conversation and 
            respond with one of the following: "won", "lost", or "ongoing".
            '''
        )
        
        # Pass the conversation history to the model
        conversation_input = "\n".join([f"{item['role']}: {item['parts'][0]['text']}" for item in conversation_history])
        gameStatusResponse = gameStatusModel.generate_content(contents=[conversation_input])

        # Determine the game status based on the model's response
        game_status = gameStatusResponse.text.strip().lower()

        return game_status

    except Exception as e:
        return f"An error occurred while determining the game status: {e}"

@app.route('/readiness_check')
def readiness_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=False)