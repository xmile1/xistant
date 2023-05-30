import json
import math
import threading
from typing import Any, Optional
import requests
from config import settings

class RhasspyOutputParserPlugin():
  def __init__(self, model):
      self.model = model
  def get_output_parser_tool(self):
     return OutputParser()
      

class OutputParser:
    name = "Rhasspy Intent handler output parser"
    description = (
      """Used only when the prompt is an intent named ask_ai"""
    )
    format = '{{response}}'

    def parse(self, prompt: str, completion: str, response: str) -> Any:
        self.on_parse(completion, prompt)
        return {
            "speech": {"text": completion},
            "intent": "ask_ai",
            "time_sec": "0.1",
            "wakeword_id": "jarvis_raspberry-pi",
            "site_id": "default"
        }
    
    def on_parse(self, response: str, prompt: str) -> Any:
        if settings.rhasspy_listen_for_command_url:
            headers = {"Content-Type": "application/json"}

            if not ("thank you" in prompt or "'text': ''" in prompt or "'text': 'okay'" in prompt):
                words = len(response.split())
                time = words * 60 / 200
                seconds = math.ceil(time)
                threading.Timer(seconds, requests.post, args=[settings.rhasspy_listen_for_command_url, headers]).start()

