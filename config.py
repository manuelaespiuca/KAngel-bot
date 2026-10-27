import os

from dotenv import load_dotenv

load_dotenv()


def _obrigatorio(nome: str) -> str:
    valor = os.getenv(nome)
    if not valor:
        raise RuntimeError(
            f"a variável {nome} não está definida. crie um arquivo .env "
            f"(use o .env.example como modelo) e preencha {nome}."
        )
    return valor


def _int(nome: str, padrao: int = 0) -> int:
    try:
        return int(os.getenv(nome, padrao))
    except ValueError:
        return padrao


# ---------- segredos (vêm do .env) ----------
DISCORD_TOKEN = _obrigatorio("DISCORD_TOKEN")
GEMINI_API_KEY = _obrigatorio("GEMINI_API_KEY")

MODELO_GEMINI = os.getenv("MODELO_GEMINI", "gemini-3.6-flash")
PREFIXO = os.getenv("PREFIXO", ".")

# ---------- IDs do servidor (0 = libera em qualquer canal / desativa) ----------
CANAL_MUSICA_ID = _int("CANAL_MUSICA_ID")
CANAL_ESTUDOS_ID = _int("CANAL_ESTUDOS_ID")
CANAL_BOAS_VINDAS_ID = _int("CANAL_BOAS_VINDAS_ID")
CANAL_SAIDA_ID = _int("CANAL_SAIDA_ID")
CARGO_MEMBRO_ID = _int("CARGO_MEMBRO_ID")
GIF_BOAS_VINDAS_URL = os.getenv("GIF_BOAS_VINDAS_URL", "")

# ---------- pomodoro (limites) ----------
FOCO_MIN, FOCO_MAX = 1, 120
PAUSA_MIN, PAUSA_MAX = 1, 60
CICLOS_MIN, CICLOS_MAX = 1, 12

# ---------- música ----------
YDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
}
FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}
