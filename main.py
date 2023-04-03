# A python package that contains a class with a function that calls open ai and returns the result

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
    
    def get_token():
      res = requests.get('https://my-open-ai.onrender.com/token')
      return res.json()['token']

    
    
