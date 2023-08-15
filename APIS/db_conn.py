#import os
import config
#import json

import pyodbc
from fastapi import APIRouter




router = APIRouter(prefix='/db_connection', tags=['Database Connection'], 
                   responses={404: {"message":"No encontrado"}})



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



@router.get("/BookStore")
async def get_top_table():
    return fetch_from_db('SELECT TOP 1000 * FROM DBO.BOOKSTORE')


@router.get("/Query")
async def get_table(sql_query):
    return fetch_from_db(sql_query)


def fetch_from_db(sql_query: str) -> str:
    cursor.execute(sql_query)
    results = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    return results

