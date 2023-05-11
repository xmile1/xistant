import os
from langchain.agents import load_tools


os.environ["GOOGLE_CSE_ID"] = "273b549453e984fbd"
os.environ["GOOGLE_API_KEY"] = "AIzaSyBV6EsWXOr4apXFD1BZ6B2POP7gw0BfvI8"

class InternetSearchPlugin:
  def __init__(self, model):
      self.model = model
  def get_lang_chain_tool(self):
     return load_tools(["google-search", "wikipedia"], llm=self.model)
  
  