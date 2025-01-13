from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

from dotenv import load_dotenv

load_dotenv()

# API connection
api_base = os.getenv("INCUBATOR_ENDPOINT")
api_key = os.getenv("INCUBATOR_KEY")


# Define the query to search for
query = """
How do I make a pancake?
"""

# Initialize the Azure OpenAI LLM
llm = AzureChatOpenAI(
    azure_endpoint=api_base,
    api_key=api_key,
    model="gpt-4o",
    api_version="2023-03-15-preview"
)

# Prepare the messages for the chat model  
messages = [  
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content=query)
]
  
# Invoke the chat model  
ai_msg = llm.invoke(messages)  
print(ai_msg.content)