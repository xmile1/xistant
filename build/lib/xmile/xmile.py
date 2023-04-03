import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from urllib.parse import urlparse
import os
import uuid

class Completion:
    async def create(self, prompt):
      token = await Completion.get_token()
      headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {token}"
      }
      data = {
          "action": "next",
          "messages": [
              {
                  "id": str(uuid.uuid4()),
                  "role": "user",
                  "content": {
                      "content_type": "text",
                      "parts": [prompt]
                  }
              }
          ],
          "model": "YOUR_MODEL_NAME_HERE",
          "parent_message_id": str(uuid.uuid4())
      }
      response = requests.post('https://chat.openai.com/backend-api/conversation', headers=headers, json=data, timeout=None, stream=True)
      response.raise_for_status()
      return response
    # await fetchSSE('https://chat.openai.com/backend-api/conversation', {
    #   method: 'POST',
    #   signal: params.signal,
    #   headers: {
    #     'Content-Type': 'application/json',
    #     Authorization: `Bearer ${this.token}`,
    #   },
    #   body: JSON.stringify({
    #     action: 'next',
    #     messages: [
    #       {
    #         id: uuidv4(),
    #         role: 'user',
    #         content: {
    #           content_type: 'text',
    #           parts: [params.prompt],
    #         },
    #       },
    #     ],
    #     model: modelName,
    #     parent_message_id: uuidv4(),
    #   }),
    #  write code to call https://chat.openai.com/backend-api/conversation
    #  and return the result
      headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
      }
      res = requests.post('https://chat.openai.com/backend-api/conversation', headers=headers, data=data)

      return res.json()
    
    async def get_token():
      res = await requests.get('https://my-open-ai.onrender.com/token')
      return res.json()['token']
    
    def set_token(token):
      result = urlparse("postgres://eqbdenpq:DjHsjEkh0gT3bw020_J_IaYKjHgde1q2@surus.db.elephantsql.com/eqbdenpq")
      username = result.username
      password = result.password
      database = result.path[1:]
      hostname = result.hostname
      port = result.port
      conn = psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname,
        port = port
      )
      cursor = conn.cursor()
      cursor.execute("UPDATE main SET name = %s WHERE id = 1", (token,))
      conn.commit()
