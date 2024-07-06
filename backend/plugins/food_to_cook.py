from itertools import chain
from typing import Any
from langchain.agents import load_tools
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from config import settings
from langchain import LLMChain, PromptTemplate
import os

class FoodToCookPlugin():
    def __init__(self, model):
        self.model = ChatOpenAI(temperature=1.0, max_tokens=1024, client=None)
        self.theologian_prompt = PromptTemplate.from_template(
            """You are my personal chef, here is a list of food i eat. and the last series of food i ate.
            Suggest the next food i should cook for a meal.

            list of food i eat
            ===============
            {food_i_eat}
            ===============
            last series of food i ate
            ===============
            {last_series_of_food_i_ate}

            The first line of your response should be the name of the food only. Then in the next line you can speak freely in a conversational manner.
            """
        )
        self.chain = LLMChain(llm=self.model, prompt=self.theologian_prompt, verbose=True)
        
    def get_lang_chain_tool(self):
        return [FoodToCookPluginTool(chain=self.chain), AddFoodIEatTool()]

class FoodToCookPluginTool(BaseTool):
    name = "Daily FoodToCook generator"
    description = "This tool generates ideas on which food to cook for a meal"
    return_direct = True
    chain: LLMChain

    def _run(self, query: str) -> str:
        food_i_eat = "data/food_to_cook/food_i_eat.txt"
        last_series_of_food_i_ate = "data/food_to_cook/last_series_of_food_i_ate.txt"

        with open(food_i_eat, "r") as f:
            food_i_eat_content = f.read()

        with open(last_series_of_food_i_ate, "r") as f:
            last_series_of_food_i_ate_content = f.read()

        response = self.chain.run(food_i_eat=food_i_eat_content, last_series_of_food_i_ate=last_series_of_food_i_ate_content)

        suggested_food = response.split('\n')[0]

        with open(last_series_of_food_i_ate, "a") as f:
            f.write(suggested_food + "\n")

        return response
    
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("This tool does not support async")


class AddFoodIEatTool(BaseTool):
    name = "Add Food I Eat"
    description = "This tool adds food i eat to the food_i_eat.txt file, provide the name of the food only"
    return_direct = True

    def _run(self, query: str) -> str:
        food_i_eat = "data/food_to_cook/food_i_eat.txt"
        with open(food_i_eat, "a") as f:
            f.write(query + "\n")
        return "Food added to food_i_eat.txt"

    def _arun(self, query: str) -> str:
        raise NotImplementedError("This tool does not support async")
    
