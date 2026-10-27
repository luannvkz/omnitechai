import json
import os
import urllib.request

from config import MODELO, URL_API, CHAVE_API

SISTEMA = ("Você é o Omni Tech, assistente que responde SOMENTE sobre tecnologia da "
           "informação (programação, redes, hardware, software, banco de dados, "
           "segurança). Se a pergunta fugir de TI, recuse educadamente. "
           "Responda em português, de forma curta e clara.")


def responder(historico):
    """Envia o histórico para a API da Groq e devolve o texto da resposta."""
    chave = os.environ.get("GROQ_API_KEY") or CHAVE_API
    if not chave:
        return "Erro: defina a variável de ambiente GROQ_API_KEY."
    dados = {
        "model": MODELO,
        "messages": [{"role": "system", "content": SISTEMA}] + historico,
        "max_tokens": 1024,
    }
    req = urllib.request.Request(
        URL_API,
        data=json.dumps(dados).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + chave,
                 "User-Agent": "chatbot-ti/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            resp = json.loads(r.read().decode("utf-8"))
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "Erro ao chamar a API: " + str(e)
