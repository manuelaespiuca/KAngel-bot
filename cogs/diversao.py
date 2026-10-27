import random
import discord
from discord import app_commands
from discord.ext import commands

import modo_storage
from textos import TEXTOS


class Diversao(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --- .moeda / .coin (e /moeda) ---
    @commands.hybrid_command(description="sorteia cara ou coroa", aliases=["coin"])
    async def moeda(self, ctx: commands.Context):
        idioma = modo_storage.get_chave(ctx.guild.id)
        resultado = random.choice([TEXTOS[idioma]["moeda_cara"], TEXTOS[idioma]["moeda_coroa"]])
        await ctx.reply(TEXTOS[idioma]["moeda"].format(resultado=resultado))

    # --- /coin ---
    @app_commands.command(name="coin", description="flip a coin")
    @app_commands.guild_only()
    async def coin_slash(self, interaction: discord.Interaction):
        idioma = modo_storage.get_chave(interaction.guild.id)
        resultado = random.choice([TEXTOS[idioma]["moeda_cara"], TEXTOS[idioma]["moeda_coroa"]])
        await interaction.response.send_message(TEXTOS[idioma]["moeda"].format(resultado=resultado))

    # --- .dado / .dice (e /dado) ---
    @commands.hybrid_command(description="sorteia um número de 1 a 6", aliases=["dice"])
    async def dado(self, ctx: commands.Context):
        idioma = modo_storage.get_chave(ctx.guild.id)
        resultado = random.randint(1, 6)
        await ctx.reply(TEXTOS[idioma]["dado"].format(resultado=resultado))

    # --- /dice ---
    @app_commands.command(name="dice", description="rolls a number from 1 to 6")
    @app_commands.guild_only()
    async def dice_slash(self, interaction: discord.Interaction):
        idioma = modo_storage.get_chave(interaction.guild.id)
        resultado = random.randint(1, 6)
        await interaction.response.send_message(TEXTOS[idioma]["dado"].format(resultado=resultado))


async def setup(bot: commands.Bot):
    await bot.add_cog(Diversao(bot))
