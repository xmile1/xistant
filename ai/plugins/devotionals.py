import json
import os
from langchain.agents import load_tools
from langchain.tools import BaseTool
from langchain.agents.tools import Tool
import requests
from bs4 import BeautifulSoup
import random

class DevotionalsPlugin():
  def __init__(self, model):
      self.model = model
  def get_lang_chain_tool(self):
     return [GermanTeacherTool()]
  
class GermanTeacherTool(BaseTool):
  name = "Daily devotionals generator"
  description = (
    "This tool generates a daily devotional, Send me this content when i request for a daily devotional"
  )
  def _run(self, query: str) -> str: 
      url = "https://www.gty.org/library/devotionals/daily-bible"
      response = requests.get(url)

      # Parse the HTML content of the page
      soup = BeautifulSoup(response.content, "html.parser")
      devotional = soup.find('section', id='daily-bible')
      content = devotional.find('div', class_='gty-writing-content')
      content = content.text.split('Notes:')[1]
      return f"Check this content for spelling errors only, Do not summarize or rephrase it. \n {content}"

   
  async def _arun(self, query: str) -> str:
      """Use the Devotional tool asynchronously."""
      raise NotImplementedError("Daily devotional does not support async")
      
  
  