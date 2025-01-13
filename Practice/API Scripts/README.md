# Chat APIs

This folder contains Python scripts that connect to various Generative AI APIs such as ChatGPT, Gemini, and use frameworks like LangGraph/LangChain for enhanced conversational capabilities.

## Contents

### ChatGPT

- **chatGPT.py**: 
  - This script demonstrates a simple conversational chat using the ChatGPT API.
  - It loads the API key from an environment variable and initializes the OpenAI client.
  - The script sends a message to the ChatGPT model and prints the response.

### Gemini

- **geminiChat.py**: 
  - This script demonstrates a conversational chat using the Gemini 1.5 Flash model.
  - It loads the API key from an environment variable and configures the Generative AI client.
  - The script maintains a conversation history to provide context to the model.
  - It allows for user input and provides responses from the Gemini model.

### Game

- **game.py**: 
  - This script implements a text-based role-playing game using the Gemini API.
  - The AI chooses a secret role and goal, and the user interacts with the AI to uncover its identity or prevent it from achieving its goal.
  - The script includes dynamic role and goal selection, interactive gameplay, and secret identity concealment.

- **websiteGame**: 
  - This directory contains the Flask app for the web-based version of the role-playing game.
  - **app.py**: Main application file for the Flask web server.
  - **templates/index.html**: Main HTML template for the web application.
  - **static/**: Directory containing static files such as CSS, JavaScript, and images.
  - **README.md**: Instructions and examples of game usage or scenarios.
  - **.env**: Environment variables for the game.

## How to Use

1. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory and add your API keys:
     ```sh
     GEMINI_API_KEY=your_gemini_api_key_here
     chatGPT_API_KEY=your_chatgpt_api_key_here
     ```

2. **Run the Scripts**:
   - For ChatGPT:
     ```sh
     python chatGPT.py
     ```
   - For Gemini:
     ```sh
     python geminiChat.py
     ```
   - For the Role-Playing Game:
     ```sh
     python game.py
     ```

3. **Run the Flask App**:
   - Navigate to the `websiteGame` directory and run the Flask app:
     ```sh
     python app.py
     ```
   - Open your web browser and go to `http://127.0.0.1:5000` to access the game.