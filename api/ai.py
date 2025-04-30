from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx, os, json

app = FastAPI()

class Command(BaseModel):
    name: str
    args: dict

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY      = os.getenv("DEEPSEEK_API_KEY")

@app.post("/ai/command")
async def ai_command(cmd: Command):
    if cmd.name != "suggest_location":
        raise HTTPException(400, "unknown cmd")

    lat, lng = cmd.args["lat"], cmd.args["lng"]
    prompt = [
        {"role":"system","content":
         "You prioritise music concerts/venues near coordinates; "
         "if none, suggest tourist sights. Return EXACTLY 5 JSON "
         "objects with keys title, snippet, url, type."},
        {"role":"user","content":f"{lat},{lng}"}
    ]

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            DEEPSEEK_URL,
            headers={"Authorization":f"Bearer {API_KEY}",
                     "Content-Type":"application/json"},
            json={"model":"deepseek-chat","messages":prompt,"max_tokens":512}
        )
    r.raise_for_status()
    try:
        data = json.loads(r.json()["choices"][0]["message"]["content"])
    except Exception:
        raise HTTPException(500,"AI replied with bad JSON")
    return JSONResponse({"data":data})
