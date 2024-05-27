import json
from operator import index
import os
from typing import Any
from langchain.agents import load_tools
from langchain.tools import BaseTool
from langchain.agents.tools import Tool
import random

no_of_times_used = 0
index_used = 0


class GermanWordGeneratorPlugin:
    def __init__(self, model):
        self.model = model

    def get_lang_chain_tool(self):
        return [GermanWordGeneratorTool(model=self.model)]


class GermanWordGeneratorTool(BaseTool):
    name = "German new word generator"
    description = "This tool generates a new German word along with its English meaning. It is useful for expanding one's German vocabulary"
    model: Any
    return_direct = True

    def _run(self, query: str) -> str:
        global no_of_times_used, index_used
        file = open(os.path.join("data/german_words/german_phrases.txt"), "r")
        data = file.readlines()

        if no_of_times_used > 9:
            random_index = random.randint(0, len(data) - 1)
            random_index = 0
            used_line = data.pop(index_used)
            random_line = data[random_index]

            no_of_times_used = 0
            with open(os.path.join("data/german_words/german_phrases.txt"), "w") as f:
                f.writelines(data)
            with open(os.path.join("data/german_words/used_words.txt"), "a") as f:
                f.write(used_line)

            index_used = random_index
        else:
            no_of_times_used += 1
            random_line = data[index_used]

        return self.model.predict(
            f"""
        Here is a sentence in English or German, {random_line}. Return a simple sentence using the template below.
        
        Ein neues Satz für dich.
        <the sentence in english>.
        Hore in Deutsch.
        <the translation in german>.
        <the translation in german>.
        In Englisch
        <the sentence in english>.

        Example:
        Ein neues Satz für dich. 
        I want to see you again.
        Hore in Deutsch.
        Ich möchte dich wiedersehen.
        Ich möchte dich wiedersehen.
        In Englisch
        I want to see you again.
        """
        )

    async def _arun(self, query: str) -> str:
        """Use this tool asynchronously."""
        raise NotImplementedError("This tool does not support async")


def check_phrase_as_line_in_file(file_path, target_phrase):
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() == target_phrase:
                return True
        return False
