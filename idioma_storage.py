import armazenamento

ARQUIVO = "idiomas.json"
PADRAO = "pt"
IDIOMAS = ("pt", "en")

_idiomas = armazenamento.carregar(ARQUIVO, {})  # guild_id (str) -> "pt" | "en"


def get_idioma(guild_id: int) -> str:
    idioma = _idiomas.get(str(guild_id), PADRAO)
    return idioma if idioma in IDIOMAS else PADRAO


def set_idioma(guild_id: int, idioma: str) -> None:
    _idiomas[str(guild_id)] = idioma
    armazenamento.salvar(ARQUIVO, _idiomas)
