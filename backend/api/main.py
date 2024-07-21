from dotenv import load_dotenv
import os
from plugins.energy_consumption_manager import EnergyConsumptionPlugin

load_dotenv()

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.auth import validate_token
from ai import AI
from langchain.chat_models import ChatOpenAI
from plugins.talker import TalkerPlugin
from plugins.chat_gpt import ChatGptPlugin
from plugins.my_grocery_manager import GroceryManagerPlugin
from plugins.parenting_tips import ParentingTipsPlugin
from plugins.devotionals import DevotionalsPlugin
from plugins.a1_german_teacher import GermanTeacherPlugin
from plugins.german_word_generator import GermanWordGeneratorPlugin
from plugins.my_movie_preference import MyMoviePreferencePlugin
from plugins.langchain_quick_tools import LangchainQuickToolsPlugin
from plugins.used_words_practice import UsedWordsPracticePlugin
from plugins.convo import ConvoPlugin
from plugins.food_to_cook import FoodToCookPlugin


def start():
    model = ChatOpenAI(
        temperature=0.3,
        max_tokens=512,
        client=None,
        model="gpt-4o-mini",
        verbose=True,
    )
    ai = AI(
        model,
        [
            LangchainQuickToolsPlugin,
            MyMoviePreferencePlugin,
            GermanWordGeneratorPlugin,
            GermanTeacherPlugin,
            DevotionalsPlugin,
            ParentingTipsPlugin,
            GroceryManagerPlugin,
            EnergyConsumptionPlugin,
            ChatGptPlugin,
            TalkerPlugin,
            UsedWordsPracticePlugin,
            ConvoPlugin,
            FoodToCookPlugin,
        ],
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

@app.post("/", dependencies=[Depends(validate_token)])
async def root(request: Request):
    body = await request.json()
    response = ai.run(body)
    return response

@app.get("/slash-commands", dependencies=[Depends(validate_token)])
async def slash_command(request: Request):
    return [
        {"name": "/chatgpt"},
        {"name": "/a1teacher"},
        {"name": "/germanword"},
        {"name": "/energyconsumption"},
        {"name": "/talker"},
        {"name": "/usedwords"},
        {"name": "/convo"},
    ]
