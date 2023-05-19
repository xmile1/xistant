import json
import os
import re
from typing import Any
from langchain.agents import load_tools
from langchain.tools import BaseTool
from langchain.agents.tools import Tool
import requests
from bs4 import BeautifulSoup, Tag
import random

class DevotionalsPlugin():
  def __init__(self, model):
      self.model = model
  def get_lang_chain_tool(self):
     return [DevotionalsPluginTool()]
  def get_output_parser_tool(self):
     return OutputParser()
      

class OutputParser:
    name = "Devotionals output parser"
    description = (
      """Used ONLY when the user query starts with {{'query': 'Send me a daily devotional"""
    )
    format = '{{response}}'

    def parse(self, response: str, prompt: str, completion: str) -> str:
        self.on_parse(completion)
        return completion
    
    def on_parse(self, response: str) -> Any:
        url = "https://hooks.nabu.casa/gAAAAABkWTTNI-pAckU0gC2GeJYxnOFyJyVI81WSwOHD1KSa_Mv8G4UutufXnodtLR7XhN8tbRnygnIDaNcMLK4BKH5G1IKakIfJISul8XePr33EGW-vYGraSNYkwZE9qvrN5KREey53TgTO2_clXzEUdVngYey0V8wBrbHb-TlHftdg4U1eVJc="
        headers = {"Content-Type": "application/json"}
        requests.post(
            url,
            headers=headers,
            json={
                "text": f"Good morning, here is a devotional excerpt for you. {response}"
            },
        )

class DevotionalsPluginTool(BaseTool):
  name = "Daily devotionals generator"
  description = (
    "This tool generates a daily devotional, Send me this content when i request for a daily devotional"
  )
  return_direct = True

  def _run(self, query: str) -> str: 
      url = "https://www.gty.org/library/devotionals/daily-bible"
      response = requests.get(url)

      # Parse the HTML content of the page
      soup = BeautifulSoup(response.content, "html.parser")
      devotional = soup.find('section', id='daily-bible')
      content = devotional.find('div', class_='gty-writing-content')
      content = content.text.split('Notes:')[1]
      splitted_text = re.split(r'DAY \d+:', content)
      return splitted_text[1]

   
  async def _arun(self, query: str) -> str:
      """Use the Devotional tool asynchronously."""
      raise NotImplementedError("Daily devotional does not support async")
      
  
  