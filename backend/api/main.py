from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from ai import AI
from langchain.chat_models import ChatOpenAI
from plugins.german_ai_output_parser import GermanAIOutputParserPlugin
from plugins.my_grocery_manager import GroceryManagerPlugin
from plugins.parenting_tips import ParentingTipsPlugin
from plugins.rhasspy_output_parser import RhasspyOutputParserPlugin
from plugins.gty_devotionals import DevotionalsPlugin
from plugins.a1_german_teacher import GermanTeacherPlugin
from plugins.german_word_generator import GermanWordGeneratorPlugin
from plugins.my_movie_preference import MyMoviePreferencePlugin
from plugins.langchain_quick_tools import InternetSearchPlugin

def start():
    model = ChatOpenAI(temperature=0.3, max_tokens=512, client=None)
    ai = AI(
        model,
        [
            InternetSearchPlugin,
            MyMoviePreferencePlugin,
            GermanWordGeneratorPlugin,
            GermanTeacherPlugin,
            DevotionalsPlugin,
            RhasspyOutputParserPlugin,
            GermanAIOutputParserPlugin,
            ParentingTipsPlugin,
            GroceryManagerPlugin,
        ]
    )
    return ai

ai = start()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/")
async def root(request: Request):
    body = await request.json()
    response = ai.run(body)
    return response


from api import local_endpoint
app.mount('/', local_endpoint.router)
