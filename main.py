from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT, build_prompt
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI(title="Sistema de Evolução Real")

class DadosDiarios(BaseModel):
    tipo: str = "diario"
    treino: str | None = None
    estudo_horas: float | None = None
    produtividade: int | None = None
    energia: int | None = None
    observacoes: str | None = None
    treino_dias: int | None = None

@app.post("/analisar")
async def analisar(dados: DadosDiarios):
    user_prompt = build_prompt(dados.model_dump())

    try:
        resposta = model.generate_content(SYSTEM_PROMPT + "\n\n" + user_prompt)
        analise = resposta.text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API: {str(e)}")

    return {"tipo": dados.tipo, "analise": analise}

@app.get("/")
def root():
    return {"status": "ok", "sistema": "Evolução Real"}
