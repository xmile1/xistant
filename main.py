import psycopg2
import requests

class Completion:
    def create(prompt):
    #  call
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
    
    def get_token():
      res = requests.get('https://my-open-ai.onrender.com/token')
      return res.json()['token']
    
    def set_token(self, token):
      conn = psycopg2.connect(database="db_name",
              host="db_host",
              user="db_user",
              password="db_pass",
              port="db_port")
      cursor = conn.cursor()
      cursor.execute("INSERT INTO tokens (token) VALUES (%s)", (token,))
      conn.commit()
