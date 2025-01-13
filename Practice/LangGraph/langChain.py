import os
from dotenv import load_dotenv
load_dotenv()

model = "openai"  # CHOOSE MODEL: "openai", "ollama", "google", "anthropic"
prompt = "What is the capital of France?"

try:
    if model == "openai":
        from langchain_openai import OpenAI
        openai_api_key = os.getenv("chatGPT_API_KEY")
        llm = OpenAI(api_key=openai_api_key)
        response = llm.invoke(prompt)
    elif model == "ollama":
        from langchain_ollama import OllamaLLM
        llm = OllamaLLM(model="llama3")
        response = llm.invoke(prompt)
    elif model == "google":
        from langchain_google_vertexai import ChatVertexAI
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        llm = ChatVertexAI(model_name="gemini-1.5-flash", api_key=GEMINI_API_KEY)
        response = llm.invoke(prompt)
    elif model == "anthropic":
        from langchain_anthropic import ChatAnthropic
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        llm = ChatAnthropic(model_name="claude-3-5-haiku-latest", api_key=anthropic_api_key)
        response = llm.invoke(prompt)
        #response = response["content"]
    else:
        raise ValueError("Invalid model type specified.")

    # Generate a response
    print(response)

except Exception as e:
    print(f"An error occurred: {e}")
