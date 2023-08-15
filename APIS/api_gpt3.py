import os
import openai
import config
from pydantic import BaseModel
#from typing import Optional
from fastapi import APIRouter

#import typer

openai.api_key = config.OPENAI_API_KEY

router = APIRouter(prefix='/GPT3.5', tags=['GPT3.5'], 
                   responses={404: {"message":"No encontrado"}})


class Prompt(BaseModel):
    role: str
    content: str


# Contexto del asistente
context = {
        "role": "system",
        "content": "Eres un asistente experto en promps, bases de datos y programación. Solo respondes una vez como 'Asistente'"
    }
messages = [context]



@router.get("/memory")
async def get_messages():
    return messages


@router.get("/{prompt_input}")
async def products(prompt_input : str):
    content = prompt_input

    messages.append({"role": "user", "content": content})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    response_content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": response_content})
    
    return response_content
    

    

    









