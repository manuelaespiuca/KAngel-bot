import asyncio
from discord.ext import commands

import config
import modo_storage
from textos import TEXTOS


class Pomodoro(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sessoes = {}  # user_id -> asyncio.Task (as sessões se perdem se o bot reiniciar)

    async def _rodar(self, ctx: commands.Context, foco: int, pausa: int, ciclos: int):
        idioma = modo_storage.get_chave(ctx.guild.id)
        t = TEXTOS[idioma]
        mention = ctx.author.mention

        try:
            for n in range(1, ciclos + 1):
                await asyncio.sleep(foco * 60)

                if n == ciclos:
                    await ctx.channel.send(t["foco_fim"].format(mention=mention, total=ciclos))
                    break

                await ctx.channel.send(t["foco_pausa"].format(mention=mention, n=n, total=ciclos, pausa=pausa))
                await asyncio.sleep(pausa * 60)
                await ctx.channel.send(t["foco_volta"].format(mention=mention, n=n + 1, total=ciclos, foco=foco))
        finally:
            if self.sessoes.get(ctx.author.id) is asyncio.current_task():
                self.sessoes.pop(ctx.author.id, None)

    @commands.hybrid_command(description="inicia uma sessão de foco (pomodoro)", aliases=["focus"])
    async def foco(self, ctx: commands.Context, foco: int = 25, pausa: int = 5, ciclos: int = 4):
        idioma = modo_storage.get_chave(ctx.guild.id)
        t = TEXTOS[idioma]

        if ctx.author.id in self.sessoes:
            await ctx.reply(t["foco_ja_ativo"])
            return

        if not (config.FOCO_MIN <= foco <= config.FOCO_MAX
                and config.PAUSA_MIN <= pausa <= config.PAUSA_MAX
                and config.CICLOS_MIN <= ciclos <= config.CICLOS_MAX):
            await ctx.reply(t["foco_invalido"].format(
                foco_min=config.FOCO_MIN, foco_max=config.FOCO_MAX,
                pausa_min=config.PAUSA_MIN, pausa_max=config.PAUSA_MAX,
                ciclos_min=config.CICLOS_MIN, ciclos_max=config.CICLOS_MAX,
            ))
            return

        await ctx.reply(t["foco_inicio"].format(
            mention=ctx.author.mention, ciclos=ciclos, foco=foco, pausa=pausa
        ))
        self.sessoes[ctx.author.id] = asyncio.create_task(self._rodar(ctx, foco, pausa, ciclos))

    @commands.hybrid_command(description="encerra sua sessão de foco", aliases=["stopfocus"])
    async def pararfoco(self, ctx: commands.Context):
        idioma = modo_storage.get_chave(ctx.guild.id)
        tarefa = self.sessoes.pop(ctx.author.id, None)

        if tarefa is None:
            await ctx.reply(TEXTOS[idioma]["foco_nenhum"])
            return

        tarefa.cancel()
        await ctx.reply(TEXTOS[idioma]["foco_parado"])

    async def cog_unload(self):
        for tarefa in self.sessoes.values():
            tarefa.cancel()


async def setup(bot: commands.Bot):
    await bot.add_cog(Pomodoro(bot))
