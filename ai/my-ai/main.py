import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import ChatOpenAI
from ai.my_ai import MyAI
from plugins.german_ai_output_parser import GermanAIOutputParserPlugin
from plugins.parenting_tips import ParentingTipsPlugin
from plugins.rhasspy_output_parser import RhasspyOutputParserPlugin
from plugins.devotionals import DevotionalsPlugin
from plugins.german_teacher import GermanTeacherPlugin
from plugins.german_word_generator import GermanWordGeneratorPlugin
from plugins.my_movie_preference import MyMoviePreferencePlugin
from plugins.internet_search import InternetSearchPlugin

os.environ["OPENAI_API_KEY"] = "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"

def start():
    model = ChatOpenAI(
        temperature=0.3,
        max_tokens=512
    )

    ai = MyAI(
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
    response = ai.handle_request(body)
    return response


@app.post("/text-to-intent")
async def text_to_intent(request: Request):
    body = await request.body()
    # return a Rhasppy intent
    return {
        "intent": {"name": "ask_ai", "confidence": 1.0},
        "entities": [{"value": body, "entity": "query", "start": 0, "end": len(body)}],
        "slots": {
            "query": body,
        },
        "siteId": "default",
        "id": "93bee187-816f-4db4-a615-4a7c9e3c0e07",
        "sessionId": "93bee187-816f-4db4-a615-4a7c9e3c0e07",
    }
