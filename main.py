import logging
import os
import pathlib

# Faz o bot sempre rodar a partir da pasta onde está este main.py,
# não importa de onde o VS Code (ou o terminal) mandou rodar.
PASTA = pathlib.Path(__file__).resolve().parent
os.chdir(PASTA)

import discord
from discord.ext import commands
from google import genai
from google.genai import types

import config
import modo_storage
from textos import TEXTOS

intents = discord.Intents.default()
intents.message_content = True  # ia.py e os comandos com prefixo precisam disso
intents.members = True          # boas-vindas / saída


class Bot(commands.Bot):
    async def setup_hook(self):
        # membros expulsos/banidos por comando: não mandar a mensagem de "saiu do servidor"
        self.saida_silenciosa = set()
        self.cogs_ok = 0

        # o cliente do Gemini precisa existir ANTES de carregar ia.py e tutor.py
        # timeout em milissegundos: cada tentativa desiste sozinha depois de 30s
        self.genai_client = genai.Client(
            api_key=config.GEMINI_API_KEY,
            http_options=types.HttpOptions(timeout=30000),
        )

        arquivos = sorted((PASTA / "cogs").glob("*.py"))
        if not arquivos:
            print(f"[aviso] nenhum cog encontrado em {PASTA / 'cogs'}")

        for arquivo in arquivos:
            if arquivo.stem.startswith("_"):
                continue
            try:
                await self.load_extension(f"cogs.{arquivo.stem}")
                self.cogs_ok += 1
            except Exception as e:
                print(f"[erro] cog {arquivo.stem} falhou: {type(e).__name__}: {e}")

        await self.tree.sync()  # registra os comandos com /


bot = Bot(command_prefix=config.PREFIXO, intents=intents)


@bot.check
async def so_em_servidor(ctx: commands.Context):
    # todos os comandos usam ctx.guild, então não funcionam em DM
    if ctx.guild is None:
        raise commands.NoPrivateMessage()
    return True


@bot.event
async def on_ready():
    print(f"bot online como {bot.user} | {bot.cogs_ok} cogs carregados")


@bot.event
async def on_command_error(ctx: commands.Context, erro):
    if isinstance(erro, (commands.CommandNotFound, commands.NoPrivateMessage)):
        return
    if ctx.command is not None and ctx.command.has_error_handler():
        return  # o próprio comando já trata (kick, ban, painel)
    if isinstance(erro, (commands.MissingRequiredArgument, commands.BadArgument)):
        idioma = modo_storage.get_chave(ctx.guild.id)
        await ctx.reply(TEXTOS[idioma]["erro_argumento"])
        return
    print(f"erro no comando {ctx.command}: {erro}")


bot.run(config.DISCORD_TOKEN, log_level=logging.WARNING)