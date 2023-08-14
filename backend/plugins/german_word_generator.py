import json
import os
from typing import Any
from langchain.agents import load_tools
from langchain.tools import BaseTool
from langchain.agents.tools import Tool
import requests
from bs4 import BeautifulSoup
import random

class GermanWordGeneratorPlugin():
  def __init__(self, model):
      self.model = model
  def get_lang_chain_tool(self):
     return [GermanWordGeneratorTool(model=self.model)]
  
class GermanWordGeneratorTool(BaseTool):
  name = "German new word generator"
  description = (
    "This tool generates a new German word along with its English meaning. It is useful for expanding one's German vocabulary"
  )
  model: Any
  return_direct = True
  
  def _run(self, query: str) -> str: 
      file = open(os.path.join("data/german_words/german_words.txt"), "r")
      data = file.readlines()

      random_index = random.randint(0, len(data) - 1)
      random_line = data.pop(random_index)

      was_used_before = check_phrase_as_line_in_file(os.path.join("data/german_words/used_words.txt"), random_line)

      if was_used_before:
        with open(os.path.join("data/german_words/german_words.txt"), "w") as f:
          f.writelines(data)
      else:
        with open(os.path.join("data/german_words/used_words.txt"), "a") as f:
         f.write(random_line)

      return self.model.predict(f'''
        Here is a german word and its meaning, {random_line}. Return a simple sentence using the template below 
        
        Here\'s a new word for you. <new word>. It means. <meaning>. 
        listen again.
        <new word>. 
        It means. <meaning>.''')

   
  async def _arun(self, query: str) -> str:
      """Use the GoogleAssit tool asynchronously."""
      raise NotImplementedError("Google assist does not support async")


def check_phrase_as_line_in_file(file_path, target_phrase):
  with open(file_path, 'r') as file:
      lines = file.readlines()
      for line in lines:
          if line.strip() == target_phrase:
              return True
      return False
