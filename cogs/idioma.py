from discord.ext import commands

import idioma_storage
import modo_storage
from textos import TEXTOS


class Idioma(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(description="troca o idioma do bot neste servidor (pt ou en)", aliases=["language"])
    async def idioma(self, ctx: commands.Context, idioma: str):
        idioma = idioma.lower()

        if idioma not in ("pt", "en"):
            atual = modo_storage.get_chave(ctx.guild.id)
            await ctx.reply(TEXTOS[atual]["idioma_invalido"])
            return

        idioma_storage.set_idioma(ctx.guild.id, idioma)
        chave = modo_storage.get_chave(ctx.guild.id)
        await ctx.reply(TEXTOS[chave]["idioma_trocado"])


async def setup(bot: commands.Bot):
    await bot.add_cog(Idioma(bot))
