import asyncio

import discord
import yt_dlp
from discord import app_commands
from discord.ext import commands

import config
import modo_storage
from textos import TEXTOS


class Musica(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.filas_musica = {}

    def tocar_proxima(self, canal, vc, erro=None):
        if erro:
            print(f"erro durante a reprodução: {erro}")

        if not vc.is_connected():
            return

        fila = self.filas_musica.get(vc.guild.id, [])
        if not fila:
            return

        titulo, url_audio = fila.pop(0)
        fonte = discord.FFmpegPCMAudio(url_audio, **config.FFMPEG_OPTIONS)
        vc.play(fonte, after=lambda e: self.tocar_proxima(canal, vc, e))

        idioma = modo_storage.get_chave(vc.guild.id)
        asyncio.run_coroutine_threadsafe(
            canal.send(TEXTOS[idioma]["tocar_tocando"].format(titulo=titulo)), self.bot.loop
        )

    async def _tocar_logica(self, canal, autor, guild, enviar_resposta, busca: str):
        """Lógica compartilhada entre .tocar/.play e /tocar/play, pra não duplicar código."""
        idioma = modo_storage.get_chave(guild.id)

        # CANAL_MUSICA_ID = 0 libera em qualquer canal
        if config.CANAL_MUSICA_ID and canal.id != config.CANAL_MUSICA_ID:
            await enviar_resposta(TEXTOS[idioma]["tocar_canal_errado"].format(canal=config.CANAL_MUSICA_ID))
            return

        if not autor.voice:
            await enviar_resposta(TEXTOS[idioma]["tocar_sem_voz"])
            return

        canal_voz = autor.voice.channel

        if guild.voice_client is None:
            vc = await canal_voz.connect()
        else:
            vc = guild.voice_client
            if vc.channel != canal_voz:
                await vc.move_to(canal_voz)

        await enviar_resposta(TEXTOS[idioma]["tocar_procurando"].format(busca=busca))

        def buscar_audio():
            # link direto vai direto pro yt-dlp; texto vira busca no youtube
            consulta = busca if busca.startswith(("http://", "https://")) else f"ytsearch:{busca}"
            with yt_dlp.YoutubeDL(config.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(consulta, download=False)
                if "entries" in info:
                    info = info["entries"][0]
                return info

        try:
            info = await asyncio.wait_for(asyncio.to_thread(buscar_audio), timeout=20)
        except asyncio.TimeoutError:
            await canal.send(TEXTOS[idioma]["tocar_timeout"])
            return
        except Exception as e:
            print(f"erro ao buscar música: {e}")
            await canal.send(TEXTOS[idioma]["tocar_erro"])
            return

        url_audio = info["url"]
        titulo = info.get("title", "música")

        if vc.is_playing() or vc.is_paused():
            self.filas_musica.setdefault(guild.id, []).append((titulo, url_audio))
            posicao = len(self.filas_musica[guild.id])
            await canal.send(TEXTOS[idioma]["tocar_fila"].format(posicao=posicao, titulo=titulo))
        else:
            fonte = discord.FFmpegPCMAudio(url_audio, **config.FFMPEG_OPTIONS)
            vc.play(fonte, after=lambda e: self.tocar_proxima(canal, vc, e))
            await canal.send(TEXTOS[idioma]["tocar_tocando"].format(titulo=titulo))

    # --- .tocar / .play (e /tocar) ---
    @commands.hybrid_command(description="toca uma música no canal de voz", aliases=["play"])
    async def tocar(self, ctx: commands.Context, *, busca: str):
        await ctx.defer()  # a busca demora; sem isso o /tocar falha com "o aplicativo não respondeu"
        await self._tocar_logica(ctx.channel, ctx.author, ctx.guild, ctx.send, busca)

    # --- /play ---
    @app_commands.command(name="play", description="plays a song in the voice channel")
    @app_commands.guild_only()
    @app_commands.describe(busca="song name or link")
    async def play_slash(self, interaction: discord.Interaction, busca: str):
        await interaction.response.defer()
        await self._tocar_logica(interaction.channel, interaction.user, interaction.guild, interaction.followup.send, busca)

    # --- .fila / .queue (e /fila) ---
    @commands.hybrid_command(description="mostra a fila de músicas", aliases=["queue"])
    async def fila(self, ctx: commands.Context):
        idioma = modo_storage.get_chave(ctx.guild.id)
        lista = self.filas_musica.get(ctx.guild.id, [])

        if not lista:
            await ctx.reply(TEXTOS[idioma]["fila_vazia"])
            return

        texto = "\n".join(f"{i+1}. {titulo}" for i, (titulo, _) in enumerate(lista))
        await ctx.reply(TEXTOS[idioma]["fila_atual"].format(texto=texto))

    # --- /queue ---
    @app_commands.command(name="queue", description="shows the song queue")
    @app_commands.guild_only()
    async def queue_slash(self, interaction: discord.Interaction):
        idioma = modo_storage.get_chave(interaction.guild.id)
        lista = self.filas_musica.get(interaction.guild.id, [])

        if not lista:
            await interaction.response.send_message(TEXTOS[idioma]["fila_vazia"])
            return

        texto = "\n".join(f"{i+1}. {titulo}" for i, (titulo, _) in enumerate(lista))
        await interaction.response.send_message(TEXTOS[idioma]["fila_atual"].format(texto=texto))

    # --- .pular / .skip (e /pular) ---
    @commands.hybrid_command(description="pula pra próxima música da fila", aliases=["skip"])
    async def pular(self, ctx: commands.Context):
        idioma = modo_storage.get_chave(ctx.guild.id)
        vc = ctx.guild.voice_client

        if vc and (vc.is_playing() or vc.is_paused()):
            vc.stop()
            await ctx.reply(TEXTOS[idioma]["pular"])
        else:
            await ctx.reply(TEXTOS[idioma]["sem_tocando"])

    # --- /skip ---
    @app_commands.command(name="skip", description="skips to the next song")
    @app_commands.guild_only()
    async def skip_slash(self, interaction: discord.Interaction):
        idioma = modo_storage.get_chave(interaction.guild.id)
        vc = interaction.guild.voice_client

        if vc and (vc.is_playing() or vc.is_paused()):
            vc.stop()
            await interaction.response.send_message(TEXTOS[idioma]["pular"])
        else:
            await interaction.response.send_message(TEXTOS[idioma]["sem_tocando"])

    # --- .pausar / .pause (e /pausar) ---
    @commands.hybrid_command(description="pausa a música atual", aliases=["pause"])
    async def pausar(self, ctx: commands.Context):
        idioma = modo_storage.get_chave(ctx.guild.id)
        vc = ctx.guild.voice_client

        if vc and vc.is_playing():
            vc.pause()
            await ctx.reply(TEXTOS[idioma]["pausar"])
        else:
            await ctx.reply(TEXTOS[idioma]["sem_tocando"])

    # --- /pause ---
    @app_commands.command(name="pause", description="pauses the current song")
    @app_commands.guild_only()
    async def pause_slash(self, interaction: discord.Interaction):
        idioma = modo_storage.get_chave(interaction.guild.id)
        vc = interaction.guild.voice_client

        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message(TEXTOS[idioma]["pausar"])
        else:
            await interaction.response.send_message(TEXTOS[idioma]["sem_tocando"])

    # --- .continuar / .resume (e /continuar) ---
    @commands.hybrid_command(description="retoma a música pausada", aliases=["resume"])
    async def continuar(self, ctx: commands.Context):
        idioma = modo_storage.get_chave(ctx.guild.id)
        vc = ctx.guild.voice_client

        if vc and vc.is_paused():
            vc.resume()
            await ctx.reply(TEXTOS[idioma]["continuar"])
        else:
            await ctx.reply(TEXTOS[idioma]["sem_pausado"])

    # --- /resume ---
    @app_commands.command(name="resume", description="resumes the paused song")
    @app_commands.guild_only()
    async def resume_slash(self, interaction: discord.Interaction):
        idioma = modo_storage.get_chave(interaction.guild.id)
        vc = interaction.guild.voice_client

        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message(TEXTOS[idioma]["continuar"])
        else:
            await interaction.response.send_message(TEXTOS[idioma]["sem_pausado"])

    # --- .parar / .stop (e /parar) ---
    @commands.hybrid_command(description="desconecta o bot do canal de voz", aliases=["stop"])
    async def parar(self, ctx: commands.Context):
        idioma = modo_storage.get_chave(ctx.guild.id)
        vc = ctx.guild.voice_client

        self.filas_musica.pop(ctx.guild.id, None)

        if vc:
            await vc.disconnect(force=True)
            await ctx.reply(TEXTOS[idioma]["parar"])
        else:
            await ctx.reply(TEXTOS[idioma]["sem_voz"])

    # --- /stop ---
    @app_commands.command(name="stop", description="disconnects the bot from the voice channel")
    @app_commands.guild_only()
    async def stop_slash(self, interaction: discord.Interaction):
        idioma = modo_storage.get_chave(interaction.guild.id)
        vc = interaction.guild.voice_client

        self.filas_musica.pop(interaction.guild.id, None)

        if vc:
            await vc.disconnect(force=True)
            await interaction.response.send_message(TEXTOS[idioma]["parar"])
        else:
            await interaction.response.send_message(TEXTOS[idioma]["sem_voz"])


async def setup(bot: commands.Bot):
    await bot.add_cog(Musica(bot))
