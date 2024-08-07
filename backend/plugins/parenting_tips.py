import os
from typing import Any
from langchain.agents import load_tools
from langchain.tools import BaseTool
import requests
from bs4 import BeautifulSoup
import random

class ParentingTipsPlugin():
  def __init__(self, model):
      self.model = model
  def get_lang_chain_tool(self):
     return [ParentingTipsPluginTool()]

class ParentingTipsPluginTool(BaseTool):
  name = "Daily ParentingTips generator"
  description = (
    "This tool generates parenting tips"
  )
  return_direct = True

  def _run(self, query: str) -> str: 
    used_links_path = os.path.join(os.path.dirname(__file__), "..", "data/parenting_tips/used_links.txt")
    url = "https://www.babycenter.com/sitemap-expert.xml"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "lxml")
    links = soup.find_all("loc")
    with open(used_links_path, "r") as f:
        used_links = f.read().splitlines()
    links = [link.text for link in links if link.text not in used_links and link.text.startswith("https://www.babycenter.com/baby/")]
    random_link = random.choice(links)

    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response2 = requests.get(random_link, headers=headers)
    soup = BeautifulSoup(response2.content, "html.parser")
    article = soup.find("article")
    header = article.find("h1").text
    content = article.find("div", class_="bodyText")
    for div in content.find_all("div"):
        div.decompose()
    prefix = "Hi, here is your daily parenting tip: \n\n"
    with open(used_links_path, "a") as f:
        f.write(random_link + "\n")
    return prefix + "\n\n" + header + "\n\n" + content.text[:1500]

   
  async def _arun(self, query: str) -> str:
      """Use the Devotional tool asynchronously."""
      raise NotImplementedError("This tool does not support async")
