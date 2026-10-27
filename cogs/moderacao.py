from typing import Optional

import discord
from discord.ext import commands

import modo_storage
from textos import TEXTOS


class Moderacao(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _remover(self, membro: discord.Member, motivo: str, banir: bool):
        # avisa o cog de boas-vindas pra não mandar "fulano saiu do servidor"
        self.bot.saida_silenciosa.add(membro.id)
        try:
            if banir:
                await membro.ban(reason=motivo)
            else:
                await membro.kick(reason=motivo)
        except Exception:
            self.bot.saida_silenciosa.discard(membro.id)
            raise

    @commands.hybrid_command(description="expulsa um membro do servidor")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, membro: discord.Member, *, motivo: Optional[str] = None):
        idioma = modo_storage.get_chave(ctx.guild.id)
        motivo = motivo or TEXTOS[idioma]["sem_motivo"]
        await self._remover(membro, motivo, banir=False)
        await ctx.reply(TEXTOS[idioma]["kick"].format(membro=membro, motivo=motivo))

    @commands.hybrid_command(description="bane um membro do servidor")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, membro: discord.Member, *, motivo: Optional[str] = None):
        idioma = modo_storage.get_chave(ctx.guild.id)
        motivo = motivo or TEXTOS[idioma]["sem_motivo"]
        await self._remover(membro, motivo, banir=True)
        await ctx.reply(TEXTOS[idioma]["ban"].format(membro=membro, motivo=motivo))

    @kick.error
    @ban.error
    async def erro_moderacao(self, ctx: commands.Context, erro):
        idioma = modo_storage.get_chave(ctx.guild.id)

        if isinstance(erro, commands.MissingPermissions):
            await ctx.reply(TEXTOS[idioma]["sem_permissao"])
        elif isinstance(erro, commands.MemberNotFound):
            await ctx.reply(TEXTOS[idioma]["membro_nao_encontrado"])
        elif isinstance(erro, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.reply(TEXTOS[idioma]["erro_argumento"])
        else:
            print(f"erro de moderação: {erro}")
            await ctx.reply(TEXTOS[idioma]["erro_generico"])


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderacao(bot))
