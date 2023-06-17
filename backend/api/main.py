from dotenv import load_dotenv
from plugins.energy_consumption_manager import EnergyConsumptionPlugin
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
from plugins.langchain_quick_tools import LangchainQuickToolsPlugin

def start():
    model = ChatOpenAI(temperature=0.3, max_tokens=512, client=None)
    ai = AI(
        model,
        [
            LangchainQuickToolsPlugin,
            MyMoviePreferencePlugin,
            GermanWordGeneratorPlugin,
            GermanTeacherPlugin,
            DevotionalsPlugin,
            RhasspyOutputParserPlugin,
            GermanAIOutputParserPlugin,
            ParentingTipsPlugin,
            GroceryManagerPlugin,
            EnergyConsumptionPlugin
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

@app.get("/slash-commands")
async def slash_command(request: Request):
    return [
       { "name": '/a1teacher' },
       { "name": '/germanword' },
       { "name": '/energyconsumption' },
    ]


from api import local_endpoint
app.mount('/', local_endpoint.router)