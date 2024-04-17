from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import json
import random
import sqlite3

app = FastAPI()

conn = sqlite3.connect("guesses.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS guesses (user_name text, cmc_correct int, cmc_guess int)")

with open("./ambigous_cards.json", "r") as f:
    cards = json.load(f)

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/random_card")
def random_card():
    card = random.choice(cards)
    out_json = {
        "type": card["card"][0],
        "text": card["card"][1],
        "power": card["card"][2],
        "toughness": card["card"][3],
        "loyalty": card["card"][4],
        "cmc": card["cmc"]
    }
    return out_json

@app.get("/guess")
def card_guess(user_name: str, cmc_correct: int, cmc_guess: int):
    c.execute("INSERT INTO guesses VALUES (?, ?, ?)", (user_name, cmc_correct, cmc_guess))
    conn.commit()
    return {"user_name": user_name, "cmc_correct": cmc_correct, "cmc_guess": cmc_guess}

@app.get("/guesses")
def get_guesses(user_name: str):
    c.execute("SELECT * FROM guesses WHERE user_name=?", (user_name,))
    guesses = c.fetchall()

    return {"guesses": guesses}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)