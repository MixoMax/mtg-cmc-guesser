from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import random
import sqlite3
import os

cmds = [
    "git fetch && git stash && git pull",
    "cd frontend && npm run build && cd .."
]

for cmd in cmds:
    #os.system(cmd)
    pass

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

conn = sqlite3.connect("guesses.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS guesses (user_name text, cmc_correct int, cmc_guess int)")

with open("./ambigous_cards.json", "r") as f:
    cards = json.load(f)


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

@app.get("/leaderboard")
def get_leaderboard():
    user_dict = {}
    c.execute("SELECT * FROM guesses")
    guesses = c.fetchall()

    for guess in guesses:
        name, correct, guess = guess
        is_correct = (correct == guess)
        user_dict[name] = user_dict.get(name, 0) + is_correct
    
    sorted_users = sorted(user_dict.items(), key=lambda x: x[1], reverse=True)

    out_json = []

    out_json.append(
        {
            "user_name": "user_name",
            "score": "score",
            "total_guesses": "out of",
            "avg_off_by": "avg off by"
        }
    )

    for user_name, score in sorted_users:
        out_json.append(
            {
                "user_name": user_name,
                "score": score,
                "total_guesses": len([x for x in guesses if x[0] == user_name]),
                "avg_off_by": sum([abs(x[1] - x[2]) for x in guesses if x[0] == user_name]) / len([x for x in guesses if x[0] == user_name])
            }
        )

    return JSONResponse(content=out_json)

@app.get("/")
def root():
    return FileResponse("./frontend/build/index.html")

@app.get("/{path}")
def serve_frontend(path):
    if path == "":
        path = "index.html"
    fp = f"./frontend/build/{path}"
    print(fp)
    if os.path.exists(fp):
        return FileResponse(fp)
    else:
        return JSONResponse(content={"error": "Resource not found"}, status_code=404)

@app.get("/static/{path}/{file}")
def serve_static(path, file):
    fp = f"./frontend/build/static/{path}/{file}"
    if os.path.exists(fp):
        return FileResponse(fp)
    else:
        return JSONResponse(content={"error": "Resource not found"}, status_code=404)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)