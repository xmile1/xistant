from langchain.tools import BaseTool

class MyMoviePreferencePlugin:
    def __init__(self, model):
        self.model = model
    
    def get_lang_chain_tool(self):
      return [MyPreferenceTool()]
    

class MyPreferenceTool(BaseTool):
  """Tool to get my movie preference"""

  name = "My movie preference"
  description = (
    "My movie preference, Useful for when you want to get information about my movie preference. The Input should be a question to deduce movie preference. The Input should be a question to deduce movie preference"
  )
  def _run(self, query: str) -> str: 
      return "You enjoy a variety of genres, with a particular interest in crime, mystery, and suspense. You seem to enjoy watching limited series, documentaries, and movies that explore true crime stories, investigations, and scandals. You also seem to appreciate character-driven stories that explore human relationships and emotions. Your watch history suggests that you have a diverse taste in movies, ranging from thrilling action to dark dramas and even comedies. Overall, your movie preferences indicate that you enjoy thought-provoking and engaging films that keep you on the edge of your seat."
   
  async def _arun(self, query: str) -> str:
      """Use the GoogleAssit tool asynchronously."""
      raise NotImplementedError("Google assist does not support async")
