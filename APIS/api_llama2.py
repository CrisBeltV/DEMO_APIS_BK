import os
import replicate
import config
from fastapi import APIRouter

#import typer

os.environ["REPLICATE_API_TOKEN"] = config.LLAMA_REPLICATE_API_KEY

router = APIRouter(prefix='/LLAMA2', tags=['LLAMA2'], 
                   responses={404: {"message":"No encontrado"}})

# Prompts
pre_prompt = "Eres un asistente útil. No responde como 'Usuario' ni pretende ser 'Usuario'. Solo respondes una vez como 'Asistente'"


@router.get("/{prompt_input}")
async def products(prompt_input : str):
    
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', # LLM model
                        input={"prompt": f"{pre_prompt} {prompt_input} Assistant: ", # Prompts
                        "temperature":0.1, "top_p":0.9, "max_length":300, "repetition_penalty":1})  # Model parameters
    
    full_response = ""

    for item in output:
        full_response += item
    
    return full_response








