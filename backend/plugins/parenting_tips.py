import os
from typing import Any
from langchain.agents import load_tools
from langchain.tools import BaseTool
import requests
from bs4 import BeautifulSoup
import random
from config import settings

class ParentingTipsPlugin():
  def __init__(self, model):
      self.model = model
  def get_lang_chain_tool(self):
     return [ParentingTipsPluginTool()]
  def get_output_parser_tool(self):
     return OutputParser()
      

class OutputParser:
    name = "ParentingTips output parser"
    description = (
      """Used only when the user query starts with {{'query': 'Send me a parenting tip"""
    )
    format = '{{response}}'

    def parse(self, response: str, prompt: str, completion: str) -> str:
        self.on_parse(completion)
        return completion
    
    def on_parse(self, response: str) -> Any:
      if settings.nigerian_speaker_url:
        requests.post(
            settings.nigerian_speaker_url,
            headers={"Content-Type": "application/json"},
            json={
                "text": f"Good morning, here is a parenting tip excerpt for you. {response}"
            },
        )

class ParentingTipsPluginTool(BaseTool):
  name = "Daily ParentingTips generator"
  description = (
    "This tool generates parenting tips"
  )
  return_direct = True

  def _run(self, query: str) -> str: 
    used_links_path = os.path.join(os.path.dirname(__file__), "..", "data/parenting_tips/used_links.txt")
    url = "https://journeyintoparenting.com/post-sitemap.xml"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "lxml")
    links = soup.find_all("loc")
    with open(used_links_path, "r") as f:
        used_links = f.read().splitlines()
    links = [link.text for link in links if link.text not in used_links]
    random_link = random.choice(links)

    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response2 = requests.get(random_link, headers=headers)
    soup = BeautifulSoup(response2.content, "html.parser")

    content = soup.find("div", class_="post-story")
    header = soup.find("header", class_="post-header")
    header = header.find("h1").text
    with open(used_links_path, "a") as f:
        f.write(random_link + "\n")
    return header + "\n\n" + content.text
      

   
  async def _arun(self, query: str) -> str:
      """Use the Devotional tool asynchronously."""
      raise NotImplementedError("This tool does not support async")
      
  
  