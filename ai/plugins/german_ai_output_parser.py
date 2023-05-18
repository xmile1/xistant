import json
import math
import threading
from typing import Any, Optional
import requests

class GermanAIOutputParserPlugin():
  def __init__(self, model):
      self.model = model
  def get_output_parser_tool(self):
     return OutputParser()
      

class OutputParser:
    name = "German ai speaker output parser"
    description = (
      """Used ONLY when the user query starts with {{'query': 'give me a new german word"""
    )
    format = '{{response}}'

    def parse(self, response: str, prompt: str) -> str:
        print(prompt, "prompt")
        self.on_parse(response)
        return response
    
    def on_parse(self, response: str) -> Any:
        url = "https://hooks.nabu.casa/gAAAAABkWTTt6eCMzxHXt8zgAP0XuM2MoYHy1kB2MTHA6Y35EnLXm_HotGl0zn-eo4oGmYZIblZ6lh0txubidSH2zwrqca8lFBkFEJ8LeVlXAMYE7-UnDejmOQApB6AGqApH394_9rUeoNgaPWuMnlWhrEYGMFMDYyezv4Z2PEZclP6yvHd_Oxg="
        headers = {"Content-Type": "application/json"}
        requests.post(
            url,
            headers=headers,
            json={
                "text": f"Hi there, This is your german teacher, get ready for your new word. {response}"
            },
        )

