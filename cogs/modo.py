from discord.ext import commands

import modo_storage
from textos import TEXTOS

# nomes aceitos -> modo
APELIDOS = {
    "kangel": "KAngel",
    "ame": "Ame",
    "ame-chan": "Ame",
    "amechan": "Ame",
}


class Modo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(description="troca a personalidade do bot neste servidor (KAngel ou Ame)", aliases=["mode"])
    async def modo(self, ctx: commands.Context, modo: str):
        escolhido = APELIDOS.get(modo.lower())

        if escolhido is None:
            chave = modo_storage.get_chave(ctx.guild.id)
            await ctx.reply(TEXTOS[chave]["modo_invalido"])
            return

        modo_storage.set_modo(ctx.guild.id, escolhido)
        chave = modo_storage.get_chave(ctx.guild.id)
        await ctx.reply(TEXTOS[chave]["modo_trocado"])


async def setup(bot: commands.Bot):
    await bot.add_cog(Modo(bot))
