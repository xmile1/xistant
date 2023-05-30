import re
from typing import Any
from ai.output_parser import FinalOutputParser
from langchain.agents import load_tools
from langchain.tools import BaseTool
from langchain.agents.tools import Tool
import requests
from bs4 import BeautifulSoup, Tag
import random
from config import settings

class DevotionalsPlugin():
  def __init__(self, model):
      self.model = model
      
  def get_lang_chain_tool(self):
     return [DevotionalsPluginTool()]
  
  def get_output_parser_tool(self):
     return OutputParser()


class DevotionalsPluginTool(BaseTool):
  name = "Daily devotionals generator"
  description = (
    "This tool generates a daily devotional"
  )
  return_direct = True

  def _run(self, query: str) -> str: 
      url = "https://www.gty.org/library/devotionals/daily-bible"
      response = requests.get(url)

      soup = BeautifulSoup(response.content, "html.parser")
      devotional = soup.find('section', id='daily-bible')
      if devotional is None:
        return "I'm sorry, I couldn't find a devotional for today. Please try again later."
      content = devotional.find('div', class_='gty-writing-content')
      
      content = content.text.split('Notes:')[1]
      splitted_text = re.split(r'DAY \d+:', content)
      return splitted_text[1]

   
  async def _arun(self, query: str) -> str:
      """Use the Devotional tool asynchronously."""
      raise NotImplementedError("Daily devotional does not support async")
      
  
  
class OutputParser(FinalOutputParser):
    name = "Devotionals output parser"
    description = (
      """Used only when the user query starts with 'Send me a daily devotional'"""
    )
    format = '{{response}}'

    def parse(self, completion: str, **kwargs: Any) -> str:
        self.on_parse(completion)
        return completion
    
    def on_parse(self, response: str) -> Any:
        url = settings.nigerian_speaker_url
        if url is None:
          return
        
        headers = {"Content-Type": "application/json"}
        requests.post(
            url,
            headers=headers,
            json={
                "text": f"Good morning, here is a devotional excerpt for you. {response}"
            },
        )
