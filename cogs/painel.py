import discord
from discord.ext import commands

import config
import idioma_storage

# {nome} = nome do bot, {musica} e {estudos} = canais configurados em config.py
PAINEL = {
    "pt": {
        "descricao": "cuido do servidor e organizo seus estudos.",
        "campos": [
            ("★ — conversa", "me mencione (@{nome}) ou responda uma mensagem minha e eu converso com você, sobre estudos ou qualquer outra coisa. lembro das últimas mensagens do canal pra acompanhar o assunto."),
            ("★ — estudos", "`.explicar tema` — explica de forma didática, com um exemplo\n"
                        "`.resumir texto` — resume um texto em tópicos\n"
                        "`.quiz tema` — cria 5 perguntas de múltipla escolha, com o gabarito escondido{estudos}"),
            ("★ — foco", "`.foco 25 5 4` — inicia um pomodoro: minutos de foco, minutos de pausa e quantidade de ciclos (esses são os valores padrão). eu aviso aqui quando cada etapa acabar\n"
                     "`.pararfoco` — encerra sua sessão"),
            ("★ — lembretes", "`.lembrar 2h prova` — cria um lembrete; aceita tempos como `30m`, `2h`, `1d`, `1h30m`\n"
                          "`.lembretes` — mostra seus lembretes pendentes\n"
                          "`.cancelarlembrete 3` — cancela um lembrete pelo número"),
            ("★ — tarefas", "`.tarefa texto` — adiciona uma tarefa na sua lista\n"
                        "`.tarefas` — mostra sua lista\n"
                        "`.feito 2` — marca uma tarefa como concluída, pelo número"),
            ("★ — música", "só funciona em <#{musica}>, e você precisa estar num canal de voz.\n"
                       "`.tocar nome ou link` — toca uma música; se já tiver algo tocando, entra na fila\n"
                       "`.fila` — mostra as músicas esperando\n"
                       "`.pular` — pula pra próxima da fila\n"
                       "`.pausar` — pausa a música atual\n"
                       "`.continuar` — retoma de onde parou\n"
                       "`.parar` — desconecta do canal de voz e limpa a fila"),
            ("★ — diversão", "`.moeda` — cara ou coroa\n`.dado` — sorteia de 1 a 6"),
            ("★ — moderação", "só pra quem tem permissão.\n"
                          "`.kick @pessoa motivo` — expulsa um membro\n"
                          "`.ban @pessoa motivo` — bane um membro"),
            ("★ — idioma", "`.idioma pt` ou `.idioma en` — troca o idioma das minhas respostas neste servidor"),
            ("★ — modo", "`.modo Ame` ou `.modo KAngel` — troca minha personalidade neste servidor (Ame é o tom padrão, KAngel é mais animada)"),
        ],
        "rodape": "todos os comandos também funcionam com /",
        "so_em": "\nos comandos de estudos só funcionam em <#{canal}>",
        "sem_permissao": "só administradores podem usar esse comando.",
        "aviso_fixar": "não consegui fixar a mensagem. fixe manualmente ou me dê a permissão de gerenciar mensagens.",
    },
    "en": {
        "descricao": "I take care of the server and organize your studies.",
        "campos": [
            ("★ — chat", "mention me (@{nome}) or reply to one of my messages and I'll talk with you, about studying or anything else. I remember the last messages in the channel to follow the topic."),
            ("★ — study", "`.explain topic` — explains it in a didactic way, with an example\n"
                      "`.summarize text` — summarizes a text in bullet points\n"
                      "`.quiz topic` — creates 5 multiple choice questions, with the answer key hidden{estudos}"),
            ("★ — focus", "`.focus 25 5 4` — starts a pomodoro: focus minutes, break minutes and number of cycles (these are the defaults). I'll let you know here when each stage ends\n"
                      "`.stopfocus` — ends your session"),
            ("★ — reminders", "`.remind 2h exam` — creates a reminder; accepts times like `30m`, `2h`, `1d`, `1h30m`\n"
                          "`.reminders` — shows your pending reminders\n"
                          "`.unremind 3` — cancels a reminder by its number"),
            ("★ — tasks", "`.task text` — adds a task to your list\n"
                      "`.tasks` — shows your list\n"
                      "`.done 2` — marks a task as done, by its number"),
            ("★ — music", "only works in <#{musica}>, and you need to be in a voice channel.\n"
                      "`.play name or link` — plays a song; if something is already playing, it joins the queue\n"
                      "`.queue` — shows the songs waiting\n"
                      "`.skip` — skips to the next song\n"
                      "`.pause` — pauses the current song\n"
                      "`.resume` — resumes from where it stopped\n"
                      "`.stop` — disconnects from the voice channel and clears the queue"),
            ("★ — fun", "`.coin` — heads or tails\n`.dice` — rolls 1 to 6"),
            ("★ — moderation", "only for people with permission.\n"
                           "`.kick @person reason` — kicks a member\n"
                           "`.ban @person reason` — bans a member"),
            ("★ — language", "`.language pt` or `.language en` — changes the language of my replies on this server"),
            ("★ — mode", "`.mode Ame` or `.mode KAngel` — changes my personality on this server (Ame is the default tone, KAngel is more cheerful)"),
        ],
        "rodape": "all commands also work with /",
        "so_em": "\nstudy commands only work in <#{canal}>",
        "sem_permissao": "only administrators can use this command.",
        "aviso_fixar": "I couldn't pin the message. pin it manually or give me the manage messages permission.",
    },
}


class Painel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _montar(self, idioma: str) -> discord.Embed:
        t = PAINEL[idioma]
        estudos = t["so_em"].format(canal=config.CANAL_ESTUDOS_ID) if config.CANAL_ESTUDOS_ID else ""

        embed = discord.Embed(
            description=t["descricao"],
            color=discord.Color.from_str("#f5c2e7"),
        )
        for nome_campo, valor in t["campos"]:
            embed.add_field(
                name=nome_campo,
                value=valor.format(
                    nome=self.bot.user.display_name,
                    musica=config.CANAL_MUSICA_ID,
                    estudos=estudos,
                ),
                inline=False,
            )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=t["rodape"])
        return embed

    @commands.command(aliases=["panel"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def painel(self, ctx: commands.Context):
        idioma = idioma_storage.get_idioma(ctx.guild.id)
        msg = await ctx.send(embed=self._montar(idioma))

        try:
            await msg.pin()
        except discord.HTTPException:
            await ctx.send(PAINEL[idioma]["aviso_fixar"], delete_after=15)

        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @painel.error
    async def erro_painel(self, ctx: commands.Context, erro):
        if isinstance(erro, commands.MissingPermissions):
            idioma = idioma_storage.get_idioma(ctx.guild.id)
            await ctx.reply(PAINEL[idioma]["sem_permissao"])
        else:
            print(f"erro no painel: {erro}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Painel(bot))