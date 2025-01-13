from langchain.graphs import LangGraph
from langchain.llms import Gemini

# **1. Initialize LLM**

llm = Gemini(model_name="geminix-1b", api_key="YOUR_GEMINI_API_KEY") 

# **2. Define a simple graph**

graph = LangGraph()

# **3. Add a node to the graph**

graph.add_node(
    "start",
    lambda: llm("What is the capital of France?"), 
    output_keys=["capital"] 
)

# **4. Run the graph**

result = graph.run()

# **5. Print the result**

print(f"The capital of France is: {result['capital']}")