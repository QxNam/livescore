import router as router
import auth as auth
import uvicorn
from check_conn_db import info
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values
import os

if os.path.exists('.env'):
    configs = dotenv_values(".env")
else:
    configs = os.environ

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})

@app.get("/")
def home_page():
    return {"status": "ok"}

@app.get('/mongo', response_description="All variables in the database")
def get_all_variables():
    return dict(configs)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(configs['MONGO_URL'])
    app.database = app.mongodb_client[configs['MONGO_DB']]
    app.collection = app.database[configs['MONGO_COLLECTION']]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

# including the router
app.include_router(router.router)
app.include_router(auth.router, prefix="/auth")

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)