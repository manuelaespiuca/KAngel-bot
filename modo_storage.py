import armazenamento
import idioma_storage

ARQUIVO = "modos.json"
PADRAO = "Ame"
MODOS = ("Ame", "KAngel")

_modos = armazenamento.carregar(ARQUIVO, {})  # guild_id (str) -> "Ame" | "KAngel"


def get_modo(guild_id: int) -> str:
    modo = _modos.get(str(guild_id), PADRAO)
    return modo if modo in MODOS else PADRAO


def set_modo(guild_id: int, modo: str) -> None:
    _modos[str(guild_id)] = modo
    armazenamento.salvar(ARQUIVO, _modos)


def get_chave(guild_id: int) -> str:
    """Chave pra usar em TEXTOS[...]: 'pt', 'en', 'pt-KAngel' ou 'en-KAngel'."""
    idioma = idioma_storage.get_idioma(guild_id)
    return idioma if get_modo(guild_id) == "Ame" else f"{idioma}-KAngel"
