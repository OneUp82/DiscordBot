import discord
from discord.ext import commands
from datetime import datetime

class Uke(commands.Cog):
    """Cog for å vise det nåværende ukenummeret."""

    def __init__(self, bot):
        # Lagrer bot-objektet slik at det kan brukes i metoder senere
        self.bot = bot

    @commands.command(name="uke", help="Forteller deg hvilken uke vi er i.")
    async def uke(self, ctx):
        """
        Kommando for å vise gjeldende ukenummer.
        Bruk: !uke
        """
        # Henter dagens dato og trekker ut ukenummeret ved hjelp av isocalendar()
        dagens_dato = datetime.now()
        ukenummer = dagens_dato.isocalendar()[1]

        # Lager en embed-melding med grønn farge
        embed = discord.Embed(title="📅 ", color=discord.Color.green())

        # Legger til et felt med ukenummeret
        embed.add_field(name="", value=f"Vi er i uke **{ukenummer}**!", inline=False)

        # Setter inn dagens dato nederst i embed-meldingen
        embed.set_footer(text=f"Dato: {dagens_dato.strftime('%d.%m.%Y')}")

        # Sender meldingen til den aktuelle Discord-kanalen
        await ctx.send(embed=embed)

async def setup(bot):
    """
    Registrerer cog-modulen hos boten.
    """
    await bot.add_cog(Uke(bot))