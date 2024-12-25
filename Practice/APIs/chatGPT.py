from dotenv import load_dotenv
import os
from openai import OpenAI
#import traceback

#Get API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("chatGPT_API_KEY")

try:
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role":"user","content":"Name 5 fun things to do in London."},
        ]
    )

    print(completion.choices[0].message);

#Print error
except Exception as e:
    print(f"An error occurred: {e}")
    #print("Detailed traceback:")
    #traceback.print_exc()