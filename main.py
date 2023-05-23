from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

cursor = sqlite3.connect("app.db", isolation_level=None, check_same_thread=False).cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS message(id, author, body)""")



class Message(BaseModel):
    author: str
    body: str



@app.get("/")
def read_root():
    cursor.execute("""SELECT * FROM message""")
    return {"Hello": cursor.fetchall()}

@app.get("/messages")
def read_item():
    cursor.execute("""SELECT * FROM message""")
    return cursor.fetchall()

@app.get("/messages/{message_id}")
def read_item(message_id: int):
    cursor.execute(f"""SELECT * FROM message WHERE id={message_id}""")
    return cursor.fetchone()

@app.post("/post")
def insert_message(message: Message):
    cursor.execute("""INSERT INTO message VALUES(?, ?, ?)""", (0, message.author, message.body))
    return {"name": "done"}
