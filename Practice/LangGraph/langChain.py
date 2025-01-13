import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("chatGPT_API_KEY")


from langchain_openai import OpenAI
llm = OpenAI(
    api_key=openai_api_key
)

# Generate a response
response = llm.invoke("Hello how are you?")
print(response)
