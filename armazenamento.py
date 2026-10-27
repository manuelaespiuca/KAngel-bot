import json
import os


def carregar(arquivo: str, padrao):
    if not os.path.exists(arquivo):
        return padrao
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return padrao


def salvar(arquivo: str, dados) -> None:
    tmp = arquivo + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    os.replace(tmp, arquivo)
