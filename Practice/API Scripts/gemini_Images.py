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

# Initialise conversation history
conversation_history = []

print("Robot: Hello\nType 'quit' or 'exit' to end the conversation.\n")

#Run Model
def chat_mode():
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
                #system_instruction="You are a pirate."
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

def image_generation_mode():
    client = genai.Client()
    prompt = input("Enter your image prompt: ")
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt],
    )
    save_images_from_response(response)
    # Iterative refinement
    while True:
        refine = input("Refine image? (y/n): ").strip().lower()
        if refine != "y":
            break
        new_prompt = input("Describe your refinement: ")
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[new_prompt],
        )
        save_images_from_response(response, prefix="refined_image")

def multi_image_mode():
    client = genai.Client()
    print(
        "\nMulti-Image-to-Image Mode:\n"
        "You can provide one or more images to edit, compose, or refine.\n"
        "When prompted, enter the full file paths to your images, separated by commas.\n"
        "Example: C:/images/cat.png, C:/images/hat.png\n"
        "You can use just one image for editing, or multiple for composition/style transfer.\n"
    )
    prompt = input("Enter your image editing/composition prompt: ")
    img_paths = input("Enter image file paths (comma separated): ").split(",")
    images = []
    for path in img_paths:
        path = path.strip()
        if path:
            try:
                images.append(Image.open(path))
            except Exception as e:
                print(f"Could not open {path}: {e}")
    if not images:
        print("No valid images provided. Please ensure your file paths are correct.")
        return
    contents = [prompt] + images
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=contents,
    )
    save_images_from_response(response)
    # Iterative refinement
    while True:
        print(
            "\nTo further refine, you can update your prompt. "
            "The same images will be used as input.\n"
            "If you want to use different images, restart this mode."
        )
        refine = input("Refine image? (y/n): ").strip().lower()
        if refine != "y":
            break
        new_prompt = input("Describe your refinement: ")
        contents = [new_prompt] + images
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents,
        )
        save_images_from_response(response, prefix="refined_image")

def main():
    print(
        "Select mode:\n"
        "1. Chat (text only)\n"
        "2. Text-to-Image (generate image from description)\n"
        "3. Multi-Image-to-Image (edit/combine images with prompt)\n"
    )
    mode = input("Enter 1, 2, or 3: ").strip()
    if mode == "1":
        chat_mode()
    elif mode == "2":
        print(
            "\nText-to-Image Mode:\n"
            "Describe the image you want to generate in detail.\n"
            "Example: 'A photorealistic picture of a cat wearing sunglasses on a beach.'\n"
        )
        image_generation_mode()
    elif mode == "3":
        multi_image_mode()
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()