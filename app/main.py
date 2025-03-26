# app/main.py
from fastapi import FastAPI

# FastAPI 애플리케이션 객체 정의
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}