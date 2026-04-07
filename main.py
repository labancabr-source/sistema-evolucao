from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT, build_prompt
import os

load_dotenv()

app = FastAPI(title="Sistema de Evolução Real")
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# ── Schema do input ────────────────────────────────────────────────
class DadosDiarios(BaseModel):
    tipo: str = "diario"          # "diario" ou "semanal"

    # Dados diários
    treino: str | None = None     # "sim" ou "não"
    estudo_horas: float | None = None
    produtividade: int | None = None   # 1–10
    energia: int | None = None         # 1–10
    observacoes: str | None = None

    # Dados extras para análise semanal
    treino_dias: int | None = None     # quantos dias treinou na semana


# ── Endpoint único ─────────────────────────────────────────────────
@app.post("/analisar")
async def analisar(dados: DadosDiarios):
    user_prompt = build_prompt(dados.model_dump())

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        analise = response.content[0].text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API: {str(e)}")

    return {
        "tipo": dados.tipo,
        "analise": analise,
    }


# ── Health check ───────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok", "sistema": "Evolução Real"}
