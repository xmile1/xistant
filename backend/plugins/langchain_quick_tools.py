import os
from langchain.agents import load_tools

class InternetSearchPlugin:
  def __init__(self, model):
      self.model = model
  def get_lang_chain_tool(self):
     return load_tools(["google-search", "wikipedia", "python_repl"], llm=self.model)
  
  