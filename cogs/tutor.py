import asyncio
import time

import discord
from discord.ext import commands
from google import genai
from google.genai import errors, types

import config
import modo_storage
from textos import TEXTOS

TENTATIVAS = 3  # quantas vezes tenta antes de desistir
LIMITE_TOTAL = 60  # segundos: tempo máximo esperando o Gemini (somando as tentativas)


def dividir(texto: str, limite: int = 1900):
    """Quebra o texto em pedaços que cabem numa mensagem do Discord (2000 caracteres)."""
    pedacos, atual = [], ""
    for linha in texto.split("\n"):
        while len(linha) > limite:
            if atual:
                pedacos.append(atual)
                atual = ""
            pedacos.append(linha[:limite])
            linha = linha[limite:]
        if len(atual) + len(linha) + 1 > limite:
            pedacos.append(atual)
            atual = linha
        else:
            atual = f"{atual}\n{linha}" if atual else linha
    if atual:
        pedacos.append(atual)
    return pedacos


class Tutor(commands.Cog):
    def __init__(self, bot: commands.Bot, client: genai.Client):
        self.bot = bot
        self.client = client

    def _perguntar(self, prompt: str, idioma: str) -> str:
        # roda numa thread (asyncio.to_thread), então time.sleep não trava o bot
        for i in range(TENTATIVAS):
            try:
                resposta = self.client.models.generate_content(
                    model=config.MODELO_GEMINI,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=TEXTOS[idioma]["instrucao_tutor"],
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                    ),
                )
                return resposta.text or ""
            except errors.ServerError as e:  # 5xx, tipo o 503
                if i == TENTATIVAS - 1:
                    raise
                print(f"gemini indisponível ({e.code}), tentando de novo... ({i + 1}/{TENTATIVAS - 1})")
                time.sleep(2 * (i + 1))  # espera 2s, depois 4s

    async def _responder(self, ctx: commands.Context, chave_prompt: str, entrada: str):
        idioma = modo_storage.get_chave(ctx.guild.id)

        if config.CANAL_ESTUDOS_ID and ctx.channel.id != config.CANAL_ESTUDOS_ID:
            await ctx.reply(TEXTOS[idioma]["tutor_canal_errado"].format(canal=config.CANAL_ESTUDOS_ID))
            return

        prompt = TEXTOS[idioma][chave_prompt].format(entrada=entrada)
        permitidos = discord.AllowedMentions.none()

        async with ctx.typing():
            try:
                texto = await asyncio.wait_for(
                    asyncio.to_thread(self._perguntar, prompt, idioma),
                    timeout=LIMITE_TOTAL,
                )
            except Exception as e:
                print(f"erro ao chamar o Gemini: {type(e).__name__}: {e}")
                texto = ""

        if not texto.strip():
            await ctx.reply(TEXTOS[idioma]["erro_gemini"])
            return

        for i, pedaco in enumerate(dividir(texto)):
            if i == 0:
                await ctx.reply(pedaco, allowed_mentions=permitidos)
            else:
                await ctx.send(pedaco, allowed_mentions=permitidos)

    @commands.hybrid_command(description="explica um tema de forma didática", aliases=["explain"])
    async def explicar(self, ctx: commands.Context, *, tema: str):
        await self._responder(ctx, "prompt_explicar", tema)

    @commands.hybrid_command(description="resume um texto em tópicos", aliases=["summarize"])
    async def resumir(self, ctx: commands.Context, *, texto: str):
        await self._responder(ctx, "prompt_resumir", texto)

    @commands.hybrid_command(description="cria um quiz de 5 perguntas sobre um tema")
    async def quiz(self, ctx: commands.Context, *, tema: str):
        await self._responder(ctx, "prompt_quiz", tema)


async def setup(bot: commands.Bot):
    await bot.add_cog(Tutor(bot, bot.genai_client))