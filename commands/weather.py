import aiohttp
import discord
from discord.ext import commands
import logging
from collections import defaultdict

# Definerer en Cog for værfunksjonalitet
class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)
        # Initialiserer en enkel cache for å lagre koordinater for ofte brukte byer
        self.cache = defaultdict(dict)

    # Kommando som kan brukes i Discord med "!vær <bynavn>"
    @commands.command(name="vær")
    async def vær(self, ctx, *, by: str):
        """Gir værvarsel for valgt by"""
        try:
            # Hent koordinater for byen (fra cache eller API)
            by_data = await self.hent_koordinater(by)
            if not by_data:
                await ctx.send(f"❌ Fant ikke byen '{by}'.")
                return

            lat, lon = by_data["lat"], by_data["lon"]

            # Bygg headers som kreves av MET API (inkluderer kontaktinfo i User-Agent)
            headers = {"User-Agent": "discord-weather-bot/1.0 kontakt: henrik.torres@gmail.com"}
            async with aiohttp.ClientSession() as session:
                # Henter værdata fra MET sitt API basert på koordinater
                async with session.get(f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}", headers=headers) as resp:
                    if resp.status != 200:
                        await ctx.send("❌ Klarte ikke å hente værdata.")
                        return
                    forecast = await resp.json()

            # Hent første tilgjengelige tidspunkt med værdata
            timeseries = forecast.get("properties", {}).get("timeseries", [])
            if not timeseries:
                await ctx.send("❌ Ingen tilgjengelige værdata.")
                return

            # Hent relevante detaljer som temperatur og vind
            details = timeseries[0]['data']['instant']['details']
            temperature = details.get('air_temperature', "Ukjent")
            wind = details.get('wind_speed', "Ukjent")

            # Hent værbeskrivelse som symbolkode (brukes til ikon og oversettelse)
            symbol_code = timeseries[0]['data'].get("next_1_hours", {}).get("summary", {}).get("symbol_code", "unknown")

            # Slår opp symbolkoden i en ordbok for å få norsk beskrivelse
            oversettelser = {
                "clearsky": "Klarvær", "cloudy": "Skyet", "fair": "Lettskyet", "fog": "Tåke",
                "rain": "Regn", "snow": "Snø", "thunderstorm": "Tordenvær", "unknown": "Ukjent"
            }
            norsk_forhold = oversettelser.get(symbol_code.split("_")[0], "Ukjent")

            # Bygger URL til værikon basert på symbolkoden
            ikon_url = f"https://api.met.no/weatherapi/weathericon/2.0/?symbol={symbol_code}&content_type=image/png"

            # Lager en embed for å vise værinformasjonen på en pen måte i Discord
            embed = discord.Embed(title=f"🌦️ Vær i {by.title()}", color=discord.Color.blue())
            embed.set_thumbnail(url=ikon_url)
            embed.add_field(name="🌡️ Temperatur", value=f"{temperature}°C", inline=True)
            embed.add_field(name="💨 Vind", value=f"{wind} m/s", inline=True)
            embed.add_field(name="🗒️ Forhold", value=norsk_forhold, inline=False)
            await ctx.send(embed=embed)

        except Exception as e:
            # Logger og sender feilmelding hvis noe går galt
            await ctx.send(f"❌ En feil oppstod: {e}")
            self.logger.error(f"Feil under henting av værdata: {e}")

    async def hent_koordinater(self, sted_navn: str):
        """Henter lat/lon fra OpenStreetMap med caching"""
        # Sjekk om koordinatene allerede er i cache
        if sted_navn in self.cache:
            return self.cache[sted_navn]

        async with aiohttp.ClientSession() as session:
            # Utfør spørring til Nominatim API for å finne koordinater
            async with session.get(f"https://nominatim.openstreetmap.org/search?q={sted_navn}&format=json&limit=1") as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                if not data:
                    return None

                # Lagre resultatet i cache og returner koordinatene
                self.cache[sted_navn] = {"lat": data[0]["lat"], "lon": data[0]["lon"]}
                return self.cache[sted_navn]

# Standard setup-funksjon som registrerer denne Cog-en i boten
async def setup(bot):
    await bot.add_cog(Weather(bot))

