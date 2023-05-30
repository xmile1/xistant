import json
import math
from tabnanny import verbose
import threading
from typing import Any, Optional
import requests
from config import settings

class GermanAIOutputParserPlugin():
  def __init__(self, model):
      self.model = model
  def get_output_parser_tool(self):
     return OutputParser()
      

class OutputParser:
    name = "German ai speaker output parser"
    description = (
      """This tool is exclusively used when the user query starts with "Give me a new German word."""
    )
    format = '{{response}}'

    def parse(self, completion: str, **kwargs) -> str:
        self.on_parse(completion)
        return completion
    
    def on_parse(self, response: str) -> Any:
        if not settings.german_speaker_url:
            return
        
        requests.post(
            settings.german_speaker_url,
            headers={"Content-Type": "application/json"},
            json={
                "text": f"Hi there, This is your german teacher, get ready for your new word. {response}"
            },
        )

