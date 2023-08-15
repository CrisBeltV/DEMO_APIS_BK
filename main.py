from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
#from utils.operation import sum
from APIS import api_llama2, api_gpt3, db_conn, db_gpt


app = FastAPI(
    title="Demo backend IA CHAT's 🤖🦙 💬🧾 ",
    description="Assembly, backend project with Python and FastApi. Call to API's GPT3.5 and LLAMA2.",
    summary="The project manages a basic structure of a backend with Python through routers",
    version="0.0.1",
    terms_of_service="http://127.0.0.1:8000/docs"

)

app.include_router(api_llama2.router)
app.include_router(api_gpt3.router)
app.include_router(db_conn.router)
app.include_router(db_gpt.router)


app.mount("/static", StaticFiles(directory = "static"), name = 'static')

#uvicorn main:app --reload

@app.get("/")
async def root():  
    return "¡Hola Api!"







#fetch_from_db(sql_query)

#get_top_table
#get_table
#fetch_from_db




# @app.get("/sumAct")
# async def root(n1: int, n2: int):  # request asyncronic
#     return sum(n1, n2)

