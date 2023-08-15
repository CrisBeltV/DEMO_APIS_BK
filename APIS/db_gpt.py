
import os
import openai
import pyodbc
import config
from pydantic import BaseModel
#from typing import Optional
from fastapi import APIRouter



router = APIRouter(prefix='/db_connection_GPT', tags=['Database Connection GPT'], 
                   responses={404: {"message":"No encontrado"}})



# Contexto del asistente
context = {
        "role": "system",
        "content": "Eres un asistente experto en promps, bases de datos y programación. Solo respondes una vez como 'Asistente'"
    }
messages = [context]


#DRIVER:str = os.getenv("DRIVER")
server = '(localdb)\ServidorDemos'
database = 'DB_LLMs_TEST'
username = ''
password = ''
# driver= '{ODBC Driver 17 for SQL Server}'

# Configuración de la base de datos
#server = config.SERVER
#database = config.DATABASE
#username = config.USERNAME
#password = config.PASSWORD
driver= '{ODBC Driver 17 for SQL Server}'


connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = connection.cursor()



@router.get("/memoryDB")
async def get_messages():
    return messages


# @router.get("/{prompt_input}")
# async def products(prompt_input : str):
#     content = prompt_input
#     messages.append({"role": "user", "content": content})

#     response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
#     response_content = response.choices[0].message.content
#     messages.append({"role": "assistant", "content": response_content})
    
#     return response_content


@router.get("/prompt_to_Db", tags = 'QueryBS:')
async def products(prompt_input : str):
    content = prompt_input
    if content.startswith("QueryBS: "):
        print("Mode QUERY")
        table_name = "BOOKSTORE"
        table_details = get_table_schema_and_columns(table_name)
        prompt = content.replace("QueryBS: ", "").strip()
        messages.append({"role": "user", "content": prompt})
        sql_query = get_sql_from_prompt(prompt, table_name, table_details)
        print(sql_query)

        if not sql_query:
            return "No pude generar una consulta SQL válida."
            
        results = fetch_from_db(sql_query)
        response_content = f"He encontrado {len(results)} resultados: " + ", ".join([str(result) for result in results])
        messages.append({"role": "assistant", "content": response_content})
        return response_content
    else:
        print("Mode ROL")    
        messages.append({"role": "user", "content": content})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        response_content = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response_content})
        
        return response_content
    
   




def fetch_from_db(sql_query: str) -> str:
    
    sql_query = sql_query.upper()
    print(sql_query)
    if sql_query.startswith('SELECT'):
        cursor.execute(sql_query)
        results = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return results
    else:
        #cursor.execute(sql_query)
        return 'SELECT * FROM BOOKSTORE'

    


def get_table_schema_and_columns(table_name: str) -> dict:
    cursor.execute(f"SELECT TABLE_SCHEMA, COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
    columns = cursor.fetchall()

    column_details = [
        {"name": row.COLUMN_NAME, "type": row.DATA_TYPE} for row in columns
    ]
    return column_details



def get_sql_from_prompt(prompt: str, table_name: str, table_details: list) -> str:
    """Usa GPT-3 para obtener una consulta SQL a partir de un prompt."""

    # Dado que table_details es ahora una lista, puedes crear directamente columns_detail
    columns_detail = ', '.join([f"{col['name']} ({col['type']})" for col in table_details])

    context_msg = (f"Estás trabajando con la tabla DBO.{table_name}, "  # Suponemos que el esquema es "DBO"
                   f"la cual tiene las siguientes columnas: {columns_detail}."
                   "Genera una consulta SQL Server basada en la descripción dada. "
                   "Genera únicamente la consulta, sin comentarios, textos adicionales ni saltos de línea."
                   "Recuerda que SQL Server no utiliza la cláusula LIMIT."
                   "Tu respuesta sera igual a 'sql_query' y se ejecutara con 'cursor.execute(sql_query)'."
                   """
                    Este es un ejemplo correcto de una respuesta:
                    SELECT * FROM tabla WHERE FECHA = (SELECT MIN(FECHA) FROM tabla) UNION SELECT * FROM tabla WHERE FECHA = (SELECT MAX(FECHA) tabla)
                    Este es uno incorrecto
                    SELECT TOP 1 * FROM tabla ORDER BY FECHA ASC UNION SELECT TOP 1 * FROM tabla ORDER BY FECHA DESC
                   """)
    
    messagesCont = [
        {"role": "system", "content": context_msg},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messagesCont)
    
    # result = extract_sql_from_response(response.choices[0].message.content)
    result = response.choices[0].message.content

    return result









    

    









