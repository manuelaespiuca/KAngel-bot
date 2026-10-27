import re
import time

import discord
from discord.ext import commands, tasks

import armazenamento
import modo_storage
from textos import TEXTOS

ARQUIVO = "lembretes.json"
UNIDADES = {"d": 86400, "h": 3600, "m": 60, "s": 1}
MINIMO = 10
MAXIMO = 30 * 86400


def parse_duracao(texto: str):
    """'1h30m' -> 5400 segundos. Retorna None se o formato for inválido."""
    texto = texto.lower().strip()
    if not re.fullmatch(r"(?:\d+[dhms])+", texto):
        return None
    total = sum(int(n) * UNIDADES[u] for n, u in re.findall(r"(\d+)([dhms])", texto))
    if total < MINIMO or total > MAXIMO:
        return None
    return total


class Lembretes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # (não chamar de self.lembretes: o discord.py já usa esse nome pro comando)
        self.dados = armazenamento.carregar(ARQUIVO, [])

    async def cog_load(self):
        self.checar.start()

    async def cog_unload(self):
        self.checar.cancel()

    def _salvar(self):
        armazenamento.salvar(ARQUIVO, self.dados)

    @tasks.loop(seconds=10)
    async def checar(self):
        agora = time.time()
        vencidos = [l for l in self.dados if l["due"] <= agora]
        if not vencidos:
            return

        for l in vencidos:
            self.dados.remove(l)
        self._salvar()

        for l in vencidos:
            await self._enviar(l)

    @checar.before_loop
    async def antes_de_checar(self):
        await self.bot.wait_until_ready()

    async def _enviar(self, l: dict):
        idioma = modo_storage.get_chave(l["guild"])
        msg = TEXTOS[idioma]["lembrete_chegou"].format(mention=f"<@{l['user']}>", texto=l["texto"])
        permitidos = discord.AllowedMentions(users=True, everyone=False, roles=False)

        try:
            canal = self.bot.get_channel(l["canal"])
            if canal is not None:
                await canal.send(msg, allowed_mentions=permitidos)
                return
            usuario = await self.bot.fetch_user(l["user"])
            await usuario.send(msg)
        except Exception as e:
            print(f"erro ao enviar lembrete: {e}")

    @commands.hybrid_command(description="cria um lembrete (ex: 2h prova de bio)", aliases=["remind"])
    async def lembrar(self, ctx: commands.Context, tempo: str, *, texto: str):
        idioma = modo_storage.get_chave(ctx.guild.id)
        segundos = parse_duracao(tempo)

        if segundos is None:
            await ctx.reply(TEXTOS[idioma]["lembrar_invalido"])
            return

        due = int(time.time()) + segundos
        novo_id = max((l["id"] for l in self.dados), default=0) + 1
        self.dados.append({
            "id": novo_id,
            "user": ctx.author.id,
            "guild": ctx.guild.id,
            "canal": ctx.channel.id,
            "due": due,
            "texto": texto[:500],
        })
        self._salvar()

        await ctx.reply(
            TEXTOS[idioma]["lembrar_ok"].format(ts=due, texto=texto[:500]),
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @commands.hybrid_command(description="mostra seus lembretes pendentes", aliases=["reminders"])
    async def lembretes(self, ctx: commands.Context):
        idioma = modo_storage.get_chave(ctx.guild.id)
        meus = [l for l in self.dados if l["user"] == ctx.author.id]

        if not meus:
            await ctx.reply(TEXTOS[idioma]["lembretes_vazio"])
            return

        linhas = "\n".join(
            TEXTOS[idioma]["lembrete_item"].format(id=l["id"], ts=int(l["due"]), texto=l["texto"])
            for l in sorted(meus, key=lambda l: l["due"])
        )
        await ctx.reply(
            TEXTOS[idioma]["lembretes_lista"].format(texto=linhas),
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @commands.hybrid_command(description="cancela um lembrete pelo número", aliases=["unremind"])
    async def cancelarlembrete(self, ctx: commands.Context, numero: int):
        idioma = modo_storage.get_chave(ctx.guild.id)
        alvo = next((l for l in self.dados if l["id"] == numero and l["user"] == ctx.author.id), None)

        if alvo is None:
            await ctx.reply(TEXTOS[idioma]["lembrete_inexistente"].format(id=numero))
            return

        self.dados.remove(alvo)
        self._salvar()
        await ctx.reply(TEXTOS[idioma]["lembrete_cancelado"].format(id=numero))


async def setup(bot: commands.Bot):
    await bot.add_cog(Lembretes(bot))
