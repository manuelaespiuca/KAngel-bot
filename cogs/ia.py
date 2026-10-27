import asyncio
import time

import discord
from discord.ext import commands
from google import genai
from google.genai import errors, types

import config
import modo_storage
from textos import TEXTOS
from cogs.tutor import dividir

# prefixo único do bot (se não existir em config.py, usa ".")
PREFIXO = getattr(config, "PREFIXO", ".")

TENTATIVAS = 3  # quantas vezes tenta antes de desistir
LIMITE_TOTAL = 60  # segundos: tempo máximo esperando o Gemini (somando as tentativas)


class IA(commands.Cog):
    def __init__(self, bot: commands.Bot, client: genai.Client):
        self.bot = bot
        self.client = client

    async def buscar_historico_canal(self, canal, limit=5):
        mensagens = []

        async for message in canal.history(limit=limit):
            # pula mensagens sem texto (imagem, gif, sticker...) pra não dar erro no Gemini
            if not message.content.strip():
                continue

            mensagens.append({
                "role": "model" if message.author.id == self.bot.user.id else "user",
                "parts": [{"text": message.content}],
            })

        mensagens.reverse()
        return mensagens

    def ask_gpt(self, mensagens, idioma):
        # roda numa thread (asyncio.to_thread), então time.sleep não trava o bot
        for i in range(TENTATIVAS):
            try:
                resposta = self.client.models.generate_content(
                    model=config.MODELO_GEMINI,
                    contents=mensagens,
                    config=types.GenerateContentConfig(
                        system_instruction=TEXTOS[idioma]["instrucao_conversa"],
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                    ),
                )
                return resposta.text or ""
            except errors.ServerError as e:  # 5xx, tipo o 503
                if i == TENTATIVAS - 1:
                    raise
                print(f"gemini indisponível ({e.code}), tentando de novo... ({i + 1}/{TENTATIVAS - 1})")
                time.sleep(2 * (i + 1))  # espera 2s, depois 4s

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return

        # ignora comandos com prefixo
        if message.content.startswith(PREFIXO):
            return

        e_resposta_ao_bot = (
            message.reference is not None
            and message.reference.resolved is not None
            and getattr(message.reference.resolved, "author", None) == self.bot.user
        )
        foi_mencionado = self.bot.user in message.mentions

        if not foi_mencionado and not e_resposta_ao_bot:
            return

        idioma = modo_storage.get_chave(message.guild.id)

        async with message.channel.typing():
            mensagens = await self.buscar_historico_canal(message.channel)
            if not mensagens:
                return

            try:
                texto = await asyncio.wait_for(
                    asyncio.to_thread(self.ask_gpt, mensagens, idioma),
                    timeout=LIMITE_TOTAL,
                )
            except Exception as e:
                print(f"erro ao chamar o Gemini: {type(e).__name__}: {e}")
                texto = ""

        if not texto.strip():
            await message.reply(TEXTOS[idioma]["erro_gemini"])
            return

        permitidos = discord.AllowedMentions.none()
        for i, pedaco in enumerate(dividir(texto)):
            if i == 0:
                await message.reply(pedaco, allowed_mentions=permitidos)
            else:
                await message.channel.send(pedaco, allowed_mentions=permitidos)


async def setup(bot: commands.Bot):
    await bot.add_cog(IA(bot, bot.genai_client))