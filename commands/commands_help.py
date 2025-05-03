import discord
from discord.ext import commands

class HelpCommands(commands.Cog):
    """Cog for å vise en oversikt over alle tilgjengelige kommandoer."""

    def __init__(self, bot):
        # Lagre referanse til boten for å hente kommandoer senere
        self.bot = bot

    @commands.command(name="hjelp", help="Viser en oversikt over alle tilgjengelige kommandoer.")
    async def hjelp(self, ctx, visningsmodus: str = "privat"):
        """
        Viser hjelpemenyen med en liste over alle tilgjengelige kommandoer.
        Bruk: !hjelp [her|privat]
        'her' viser hjelpen i kanalen, 'privat' sender den som DM (standard).
        """
        embed = discord.Embed(
            title="📚 Hjelpemeny",
            description="Her er en liste over kommandoene du kan bruke:",
            color=discord.Color.blurple()
        )

        # Liste over kategorier og tilhørende kommandoer
        kategorier = {
            "📰 Nyheter / PDF": ["pdf", "nyheter"],
            "🌤️ Vær": ["vær"],
            "🚌 Reiseplanlegger": ["tur"],
            "🔎 Søkemotorer": ["google", "bing"],
            "📅 Ukekommandoer": ["uke"],
            "🎵 Musikk": ["yt", "pause", "fortsett", "skip", "yt-liste", "tømkø"],
            "🆘 Hjelp": ["hjelp"]
        }

        # Går gjennom hver kategori og bygger en tekstliste over tilhørende kommandoer
        for kategori, kommandoer in kategorier.items():
            kommando_tekst = "\n".join(
                f"!{cmd} – {self.bot.get_command(cmd).help}" 
                for cmd in kommandoer 
                if self.bot.get_command(cmd)  # Sjekker at kommandoen faktisk finnes
            )
            embed.add_field(name=kategori, value=kommando_tekst, inline=False)

        # Sender hjelpemenyen basert på ønsket visningsmodus
        try:
            if visningsmodus.lower() == "her":
                # Viser hjelpemenyen i samme kanal som kommandoen ble brukt
                await ctx.send(embed=embed)
            else:
                # Sender hjelpemenyen som DM og varsler brukeren i kanalen
                await ctx.author.send(embed=embed)
                await ctx.message.add_reaction("📬")
                await ctx.send("📬 Hjelpemenyen er sendt til deg i DM!")

        except discord.Forbidden:
            # Bot har ikke lov til å sende DM, gir tilbakemelding
            await ctx.send("❌ Kunne ikke sende DM. Har du DMer deaktivert?")

async def setup(bot):
    """Funksjon for å registrere denne cogen når boten lastes inn."""
    await bot.add_cog(HelpCommands(bot))
