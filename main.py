from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT, build_prompt
import os

load_dotenv()

app = FastAPI(title="Sistema de Evolução Real")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=1000,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
        analise = response.choices[0].message.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API: {str(e)}")

    return {"tipo": dados.tipo, "analise": analise}

@app.get("/")
def root():
    return {"status": "ok", "sistema": "Evolução Real"}
