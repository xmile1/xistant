import json
import math
import threading
from typing import Any, Optional
import requests

class RhasspyOutputParserPlugin():
  def __init__(self, model):
      self.model = model
  def get_output_parser_tool(self):
     return OutputParser()
      

class OutputParser:
    name = "Rhasspy Intent handler output parser"
    description = (
      """Used only when the query starts with {{'intent': {{'name': 'ask_ai'"""
    )
    format = """
    {{
        "speech": {{"text": response}},
        "text": "response",
        "intent": "ask_ai",
        "time_sec": "0.1",
        "wakeword_id": "jarvis_raspberry-pi",
        "site_id": "default",
        "id": "93bee187-816f-4db4-a615-4a7c9e3c0e07",
        "sessionId": "93bee187-816f-4db4-a615-4a7c9e3c0e07"
    }}
    """

    def parse(self, response: str, prompt: str) -> str:
        response_json = json.loads(response.rstrip().lstrip())

        self.on_parse(response, prompt)
        return response_json
    
    def on_parse(self, response: str, prompt: str) -> Any:
        url = "http://192.168.0.165:12101/api/listen-for-command?timeout=60"
        headers = {"Content-Type": "application/json"}

        if "thank you" not in prompt or prompt == "" or prompt == "ok":
            words = len(response.split())
            time = words * 60 / 200
            seconds = math.ceil(time)
            threading.Timer(seconds, requests.post, args=[url, headers]).start()

