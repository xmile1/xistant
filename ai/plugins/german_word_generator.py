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
     return [GermanWordGeneratorTool()]
  
class GermanWordGeneratorTool(BaseTool):
  name = "German new word generator"
  description = (
    "it generates a new german word and its meaning in english"
  )
  return_direct = True
  def _run(self, query: str) -> str: 
      url = "https://www.coolgenerator.com/random-german-words-generator"
      response = requests.get(url)

      # Parse the HTML content of the page
      soup = BeautifulSoup(response.content, "html.parser")
      word_list = soup.find("ul", class_="list-unstyled content-list")

      words = []
      for li in word_list.find_all('li'):
          p_tags = li.find_all('p')
          word = p_tags[1].text.strip().split('-')[0]
          meaning = p_tags[2].text.strip().split(':')[1]
          words.append(f"Here is your new word. {word}. and its meaning is. {meaning}. Again the word is. {word} and its meaning is. {meaning}. and one more time the word is. {word}. and its meaning is. {meaning}.")

      return random.choice(words)

   
  async def _arun(self, query: str) -> str:
      """Use the GoogleAssit tool asynchronously."""
      raise NotImplementedError("Google assist does not support async")
