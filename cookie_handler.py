import discord
from discord.ext import commands

# Definerer en Cog-klasse for hjelpekommandoer
class HelpCommands(commands.Cog):
    def __init__(self, bot):
        # Lagre referansen til bot-objektet
        self.bot = bot

    # Registrerer kommandoen "!hjelp" med en valgfri parameter for privat visning
    @commands.command(name="hjelp", help="Viser en oversikt over alle tilgjengelige kommandoer.")
    async def hjelp(self, ctx, privat: bool = True):
        """Viser en dynamisk oversikt over tilgjengelige kommandoer."""
        
        # Lager en innebygd melding (embed) som skal inneholde hjelpeteksten
        embed = discord.Embed(
            title="📚 Hjelpemeny",
            description="Her er en liste over kommandoene du kan bruke:",
            color=discord.Color.blurple()
        )

        # Går gjennom alle tilgjengelige kommandoer i boten og legger dem til i embed
        for command in self.bot.commands:
            if not command.hidden:  # Hopper over skjulte kommandoer
                embed.add_field(
                    name=f"!{command.name}",  # Kommandoens navn, f.eks. !tur
                    value=command.help or "Ingen beskrivelse tilgjengelig.",  # Beskrivelse, eller en standardtekst
                    inline=False  # Viser én kommando per linje
                )

        try:
            if privat:
                # Sender hjelpen som privat melding (DM) til brukeren
                await ctx.author.send(embed=embed)
                # Legger til en reaksjon på kommando-meldingen for å indikere at den er sendt
                await ctx.message.add_reaction("📬")
                # Sender også en bekreftelse i kanalen
                await ctx.send("📬 Hjelpemenyen er sendt til deg i DM!")
            else:
                # Hvis privat=False, sendes hjelpen rett i kanalen
                await ctx.send(embed=embed)

        except discord.Forbidden:
            # Fanges opp hvis boten ikke har lov til å sende DM til brukeren
            await ctx.send("❌ Kunne ikke sende deg en privatmelding. Har du DMer deaktivert?")

# Obligatorisk setup-funksjon for å legge til Cog-en i boten
async def setup(bot):
    await bot.add_cog(HelpCommands(bot))