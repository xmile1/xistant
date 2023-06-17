import os
from typing import Any
from langchain.tools import BaseTool
from langchain.schema import HumanMessage

class EnergyConsumptionPlugin():
  def __init__(self, model):
      self.model = model
  def get_lang_chain_tool(self):
     return [EnergyConsumptionPluginTool(), EnergyConsumptionRetrieverPluginTool(model=self.model)]
      

class EnergyConsumptionRetrieverPluginTool(BaseTool):
  name = "EnergyConsumption retriever"
  description = (
    "The tool answers questions about energy consumption, input should be the question"
  )
  model: Any
  return_direct = True

  def _run(self, query: str) -> str:
    with open(os.path.join("data/energy_comsumption.txt"), "r") as f:
      data = f.read()
      message = [HumanMessage(content=f"""
      You are a chatbot that answers questions about energy consumption based on the data in your context, Alway provide a ready to use answer to the user and do not expect the user to do any calculations, Give estimates if necessary.

      INSTRUCTIONS:
      You will use linear interpolation to estimate values between given dates when necessary.
      First determine the data you need to answer the question, If any data is missing, use linear interpolation to estimate the missing data.

      When asked about a month, Always estimate the data for 1st or 30th/31st of the month if they are missing.

      DONOT use data for 13th as an estimate for 1st of the month or 20th as an estimate for 30th of the month. Always estimate the data for 1st or 30th/31st of the month if they are missing.
      All required data are available below

      DATA:
      {data}

      QUESTION:
      {query}

      ANSWER:
      """ )]
      return self.model(message).content


  async def _arun(self, query: str) -> str:
      """Use the tool asynchronously."""
      raise NotImplementedError("This tool does not support async")

class EnergyConsumptionPluginTool(BaseTool):
  name = "EnergyConsumption saver"
  description = (
    "Save energy consumption reading to a vector store when a user request to save his energy data, input should be the reading value in kilwatt and the date, for example 31.05.2023,13696. if the date is not provided by the user, provide today's date"
  )
  return_direct = True

  def _run(self, query: str) -> str: 
    # add the data to backend/data/energy_comsumption.txt'
    with open(os.path.join("data/energy_comsumption.txt"), "a") as f:
      f.write(f"\n{query}")
    return "Energy consumption reading saved"

  async def _arun(self, query: str) -> str:
      """Use the tool asynchronously."""
      raise NotImplementedError("This tool does not support async")
      
  
  