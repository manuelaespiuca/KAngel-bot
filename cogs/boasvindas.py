import discord
from discord.ext import commands

import config
import modo_storage
from textos import TEXTOS


def _id(nome: str) -> int:
    return getattr(config, nome, 0)


class BoasVindas(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _dar_cargo(self, membro: discord.Member):
        cargo_id = _id("CARGO_MEMBRO_ID")
        if not cargo_id:
            return  # 0 = recurso desativado
        if membro.bot or membro.pending:
            return  # pending = ainda não aceitou as regras (triagem)

        cargo = membro.guild.get_role(cargo_id)
        if cargo is None:
            print("[boas-vindas] cargo de membro não encontrado. confira o CARGO_MEMBRO_ID no config.py.")
            return
        if cargo in membro.roles:
            return

        try:
            await membro.add_roles(cargo, reason="cargo automático ao entrar")
        except discord.HTTPException as e:
            print(f"[boas-vindas] não consegui dar o cargo (o cargo do bot está acima do cargo de membro? tem 'gerenciar cargos'?): {e}")

    @commands.Cog.listener()
    async def on_member_join(self, membro: discord.Member):
        await self._dar_cargo(membro)

        canal = self.bot.get_channel(_id("CANAL_BOAS_VINDAS_ID"))
        if canal is None:
            print("[boas-vindas] canal de boas-vindas não encontrado, nada enviado.")
            return

        idioma = modo_storage.get_chave(membro.guild.id)

        embed = discord.Embed(
            description=TEXTOS[idioma]["boas_vindas"].format(mention=membro.mention),
            color=discord.Color.from_str("#f5c2e7"),
        )
        gif = getattr(config, "GIF_BOAS_VINDAS_URL", "")
        if gif:
            embed.set_image(url=gif)

        try:
            await canal.send(embed=embed)
        except discord.HTTPException as e:
            print(f"[boas-vindas] erro ao enviar (o bot tem permissão de enviar mensagens e inserir links nesse canal?): {e}")

    @commands.Cog.listener()
    async def on_member_update(self, antes: discord.Member, depois: discord.Member):
        # quem estava na triagem e acabou de aceitar as regras
        if antes.pending and not depois.pending:
            await self._dar_cargo(depois)

    @commands.Cog.listener()
    async def on_member_remove(self, membro: discord.Member):
        # saída causada por .kick/.ban já tem mensagem própria
        silenciosa = getattr(self.bot, "saida_silenciosa", set())
        if membro.id in silenciosa:
            silenciosa.discard(membro.id)
            return

        canal = self.bot.get_channel(_id("CANAL_SAIDA_ID"))
        if canal is None:
            print("[boas-vindas] canal de saída não encontrado, nada enviado.")
            return

        idioma = modo_storage.get_chave(membro.guild.id)
        try:
            await canal.send(TEXTOS[idioma]["saida"].format(membro=membro.mention))
        except discord.HTTPException as e:
            print(f"[boas-vindas] erro ao enviar a saída: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(BoasVindas(bot))