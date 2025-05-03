import discord
from discord.ext import commands

class GoogleSearch(commands.Cog):
    """Cog for å utføre Google-søk og returnere en Google-lenke."""

    def __init__(self, bot):
        # Lagrer bot-instansen for senere bruk
        self.bot = bot

    @commands.command(name="google", help="Utfør et Google-søk og få en lenke til søkeresultatene.")
    async def google(self, ctx, *, søkestreng: str):
        """
        Kommando for å generere en Google-søkelink.
        Bruk: !google <spørsmål>
        """
        # Erstatter mellomrom med '+' slik Google forstår søket
        google_url = f"https://www.google.com/search?q={søkestreng.replace(' ', '+')}"

        # Sender lenken til søkeresultatet i Discord-kanalen
        await ctx.send(f"🔎 Søker etter: **{søkestreng}** ...\n🔗 Her er Google-søket ditt: [Klikk her]({google_url})")

async def setup(bot):
    """
    Registrerer cog-modulen hos boten.
    """
    await bot.add_cog(GoogleSearch(bot))