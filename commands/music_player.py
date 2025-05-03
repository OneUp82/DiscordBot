import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import asyncio

# Konfigurasjon for yt-dlp for å hente beste tilgjengelige lyd, uten å laste ned hele videoen
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'extract_flat': False,
}

# FFmpeg-opsjoner som gjør at streamen automatisk forsøkes gjenopprettet ved avbrudd
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'  # Ikke visuell output (video fjernes)
}

# Globale variabler som holder styr på musikkø, avspillingsstatus og gjeldende sang
music_queue = []
is_playing = False
voice_client = None
current_song = None

def get_stream_url(url):
    """Henter direkte stream-URL og tittel fra en YouTube-lenke"""
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url'], info['title']

async def play_next(ctx):
    """Spiller neste sang i køen, eller kobler fra hvis køen er tom"""
    global is_playing, voice_client, current_song

    if music_queue:
        is_playing = True
        url, title = music_queue.pop(0)
        current_song = title

        try:
            # Oppretter en lydkilde fra stream-URL
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            await ctx.send(f"🎶 **Spiller nå:** {title}")

            # Når avspillingen er ferdig, spilles neste sang automatisk
            def after_playing(_):
                asyncio.run_coroutine_threadsafe(play_next(ctx), ctx.bot.loop)

            voice_client.play(source, after=after_playing)

        except Exception as e:
            await ctx.send(f"❌ Feil ved avspilling: {e}")

    else:
        # Ingen flere sanger igjen – kobler fra stemmekanal
        is_playing = False
        current_song = None
        await voice_client.disconnect()

async def setup(bot):
    @bot.command(name="yt")
    async def yt(ctx, url: str):
        """Legger til en sang i spillekø og starter avspilling hvis boten ikke spiller"""
        global is_playing, voice_client

        try:
            stream_url, title = get_stream_url(url)
            music_queue.append((stream_url, title))
            await ctx.message.add_reaction("✅")

            if not is_playing:
                # Sjekker at brukeren er i en stemmekanal før boten kobler til
                if ctx.author.voice:
                    voice_client = await ctx.author.voice.channel.connect()
                    await play_next(ctx)
                else:
                    await ctx.send("❌ Du må være i en stemmekanal for å bruke denne kommandoen!")

        except Exception as e:
            await ctx.send(f"❌ Feil: {e}")

    @bot.command(name="pause")
    async def pause(ctx):
        """Pause musikken hvis noe spiller"""
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.send("⏸️ Musikk pauset.")

    @bot.command(name="fortsett")
    async def fortsett(ctx):
        """Fortsetter musikken hvis den er pauset"""
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.send("▶️ Fortsetter musikk.")

    @bot.command(name="skip")
    async def skip(ctx):
        """Stopper nåværende sang og spiller neste"""
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("⏭️ Hopper til neste sang.")

    @bot.command(name="tømkø")
    async def tom_kø(ctx):
        """Tømmer spillekøen og stopper musikkavspilling"""
        global music_queue, is_playing, voice_client, current_song
        music_queue.clear()
        current_song = None
        if voice_client and voice_client.is_playing():
            voice_client.stop()
        if voice_client:
            await voice_client.disconnect()
        is_playing = False
        await ctx.send("🗑️ Køen er tømt og musikken er stoppet.")

    @bot.command(name="yt-liste")
    async def yt_liste(ctx):
        """Viser nåværende sang og inntil 10 sanger i køen"""
        embed = discord.Embed(title="🎵 Musikkø", color=discord.Color.green())

        # Legger til nåværende sang i embed
        if current_song:
            embed.add_field(name="🎶 Nå spiller:", value=current_song, inline=False)
        else:
            embed.add_field(name="🎶 Nå spiller:", value="Ingen musikk for øyeblikket", inline=False)

        # Viser opptil 10 sanger i køen
        if music_queue:
            kø_tekst = "\n".join(f"{i+1}. {title}" for i, (_, title) in enumerate(music_queue[:10]))
            if len(music_queue) > 10:
                kø_tekst += f"\n... og {len(music_queue) - 10} til i køen."
            embed.add_field(name="📜 Neste sanger:", value=kø_tekst, inline=False)
        else:
            embed.add_field(name="📜 Neste sanger:", value="Køen er tom.", inline=False)

        await ctx.send(embed=embed)