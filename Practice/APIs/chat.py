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

#Run Model
try:
    #Repeat questions
    while True:
        #Get user input
        userInput = str(input("What is your question? ('quit' to exit)\n")) 
        if (((userInput.lower())=="quit") or (userInput.lower())=="exit"):
            print("See you soon!")
            break

        #Run model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            #system_instruction="You are a pirate."
        )
        
        #Get token info:  Returns the "context window" for the model, which is the combined input and output token limits.
        model_info = genai.get_model("models/gemini-1.5-flash")
        print(f"{model_info.input_token_limit=}")
        print(f"{model_info.output_token_limit=}")

        #Run response
        response = model.generate_content(
            contents=userInput,
            #tools='google_search_retrieval' #Grounding in Google Search
        )
        
        #Print answer
        print("\n________")
        print(response.text)
        print("_________\nEND OF MESSAGE")
        

#Print error
except Exception as e:
    print(f"An error occurred: {e}")
