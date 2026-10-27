import discord
from discord.ext import commands

import armazenamento
import modo_storage
from textos import TEXTOS

ARQUIVO = "tarefas.json"
SEM_MENCOES = discord.AllowedMentions.none()


class Tarefas(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # (não chamar de self.tarefas: o discord.py já usa esse nome pro comando)
        self.dados = armazenamento.carregar(ARQUIVO, {})  # user_id -> [texto, ...]

    def _salvar(self):
        armazenamento.salvar(ARQUIVO, self.dados)

    @commands.hybrid_command(description="adiciona uma tarefa na sua lista", aliases=["task"])
    async def tarefa(self, ctx: commands.Context, *, texto: str):
        idioma = modo_storage.get_chave(ctx.guild.id)
        texto = texto[:200]
        self.dados.setdefault(str(ctx.author.id), []).append(texto)
        self._salvar()
        await ctx.reply(TEXTOS[idioma]["tarefa_add"].format(texto=texto), allowed_mentions=SEM_MENCOES)

    @commands.hybrid_command(description="mostra sua lista de tarefas", aliases=["tasks"])
    async def tarefas(self, ctx: commands.Context):
        idioma = modo_storage.get_chave(ctx.guild.id)
        lista = self.dados.get(str(ctx.author.id), [])

        if not lista:
            await ctx.reply(TEXTOS[idioma]["tarefas_vazio"])
            return

        texto = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(lista))
        await ctx.reply(TEXTOS[idioma]["tarefas_lista"].format(texto=texto), allowed_mentions=SEM_MENCOES)

    @commands.hybrid_command(description="marca uma tarefa como concluída (pelo número)", aliases=["done"])
    async def feito(self, ctx: commands.Context, numero: int):
        idioma = modo_storage.get_chave(ctx.guild.id)
        lista = self.dados.get(str(ctx.author.id), [])

        if not (1 <= numero <= len(lista)):
            await ctx.reply(TEXTOS[idioma]["tarefa_inexistente"].format(n=numero))
            return

        texto = lista.pop(numero - 1)
        self._salvar()
        await ctx.reply(TEXTOS[idioma]["tarefa_feita"].format(texto=texto), allowed_mentions=SEM_MENCOES)


async def setup(bot: commands.Bot):
    await bot.add_cog(Tarefas(bot))
