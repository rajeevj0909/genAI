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
from PIL import Image
from io import BytesIO

#Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

#Get API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def save_images_from_response(response, prefix="generated_image"):
    idx = 1
    for part in response.candidates[0].content.parts:
        if getattr(part, "text", None) is not None:
            print(part.text)
        elif getattr(part, "inline_data", None) is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            filename = f"{prefix}_{idx}.png"
            image.save(filename)
            print(f"Saved image: {filename}")
            idx += 1

def detect_image_intent(user_input):
    """
    Use Gemini to classify intent as IMAGE or CHAT. Falls back to keyword check on error.
    Returns True if intent is IMAGE.
    """
    try:
        classifier = genai.GenerativeModel(model_name="gemini-1.5-flash")
        system_instruction = (
            "You are an intent classifier. If the user input asks to generate, edit, compose, or otherwise produce or modify an image, "
            "respond with exactly the single word 'IMAGE'. Otherwise respond with exactly the single word 'CHAT'."
        )
        contents = [
            {"role": "system", "parts": [{"text": system_instruction}]},
            {"role": "user", "parts": [{"text": user_input}]}
        ]
        resp = classifier.generate_content(contents=contents)
        result = (resp.text or "").strip().upper()
        if result in ("IMAGE", "CHAT"):
            return result == "IMAGE"
    except Exception:
        # fall through to keyword fallback
        pass

    # Fallback: keyword-based detection (keeps previous behavior if classifier fails)
    keywords = [
        "generate image", "create image", "edit image", "compose image", "draw", "picture",
        "photo", "make image", "image of", "show me", "visualize", "illustrate"
    ]
    lowered = user_input.lower()
    return any(k in lowered for k in keywords)

def main():
    print(
        "Welcome! You can chat or ask to generate/edit images.\n"
        "To generate or edit an image, include phrases like 'generate image', 'create image', 'edit image', etc. in your prompt.\n"
        "If you want to use existing images, mention it in your prompt and you'll be asked for file paths.\n"
        "Type 'quit' or 'exit' to end the session.\n"
    )
    conversation_history = []
    while True:
        userInput = input("You: ").strip()
        if userInput.lower() in ("quit", "exit"):
            print("Robot: Bye!\n")
            break

        if detect_image_intent(userInput):
            print(
                "Do you want to use any existing images as input? (y/n)\n"
                "If yes, you'll be prompted for image file paths (comma separated)."
            )
            use_images = input("Use images? (y/n): ").strip().lower()
            images = []
            if use_images == "y":
                img_paths = input("Enter image file paths (comma separated): ").split(",")
                for path in img_paths:
                    path = path.strip()
                    if path:
                        try:
                            images.append(Image.open(path))
                        except Exception as e:
                            print(f"Could not open {path}: {e}")
                if not images:
                    print("No valid images provided. Proceeding with text prompt only.")

            contents = [userInput] + images if images else [userInput]
            image_model = genai.GenerativeModel(model_name="gemini-2.5-flash-image-preview")
            response = image_model.generate_content(contents=contents)
            save_images_from_response(response)

            # Iterative refinement using the same image_model
            while True:
                print(
                    "\nTo refine, update your prompt. "
                    "The same images will be used as input if you provided them.\n"
                    "Type 'skip' to return to main prompt."
                )
                refine = input("Refine image? (y/n): ").strip().lower()
                if refine != "y":
                    break
                new_prompt = input("Describe your refinement (or type 'skip'): ").strip()
                if new_prompt.lower() == "skip":
                    break
                contents = [new_prompt] + images if images else [new_prompt]
                response = image_model.generate_content(contents=contents)
                save_images_from_response(response, prefix="refined_image")
        else:
            # Chat mode
            conversation_history.append({
                "role": "user",
                "parts": [{"text": userInput}]
            })
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
            )
            response = model.generate_content(
                contents=conversation_history,
            )
            conversation_history.append({
                "role": "model",
                "parts": [{"text": response.text}]
            })
            print("\nRobot: " + response.text)

if __name__ == "__main__":
    main()