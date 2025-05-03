import discord
from discord.ext import commands
import aiohttp
import logging
import math
from collections import defaultdict

class TravelPlanner(commands.Cog):
    """Cog for å hente kollektivruter fra Entur API og formatere dem for Discord."""

    def __init__(self, bot):
        # Referanse til bot-instansen og oppsett av logging og cache
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)
        self.cache = defaultdict(dict)  # En enkel cache for å lagre koordinater til steder

    @commands.command(name="tur")
    async def travel_command(self, ctx, *, reise: str):
        """
        Discord-kommando for å finne reiserute mellom to steder via Entur.
        Format: !tur Fra - Til
        Eksempel: !tur Røyken - Slemmestad
        """
        try:
            # Sjekk om bruker har brukt riktig format
            if " - " not in reise:
                await ctx.send("⚠️ Formatet må være: `!tur Fra - Til`")
                return

            # Splitt brukerinput til to steder
            fra_sted, til_sted = reise.split(" - ", maxsplit=1)

            # Hent koordinater for begge steder
            from_data = await self.hent_koordinater(fra_sted)
            to_data = await self.hent_koordinater(til_sted)

            if not from_data or not to_data:
                await ctx.send("❌ Kunne ikke finne ett eller begge stedene.")
                return

            # GraphQL-spørring for å hente ruter fra Entur
            query = """ 
                query($fromLat: Float!, $fromLon: Float!, $toLat: Float!, $toLon: Float!) {
                  trip(
                    from: {coordinates: {latitude: $fromLat, longitude: $fromLon}},
                    to: {coordinates: {latitude: $toLat, longitude: $toLon}},
                    numTripPatterns: 3
                  ) {
                    tripPatterns {
                      startTime
                      endTime
                      legs {
                        mode
                        line { publicCode }
                        fromPlace { name latitude longitude }
                        toPlace { name latitude longitude }
                      }
                    }
                  }
                }
            """

            variables = {
                "fromLat": from_data["lat"],
                "fromLon": from_data["lon"],
                "toLat": to_data["lat"],
                "toLon": to_data["lon"]
            }

            # Send forespørsel til Entur sitt API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.entur.io/journey-planner/v3/graphql",
                    json={"query": query, "variables": variables}
                ) as resp:
                    data = await resp.json()

            # Hent ut reisealternativer
            trips = data.get("data", {}).get("trip", {}).get("tripPatterns", [])
            if not trips:
                await ctx.send("❌ Ingen ruter funnet.")
                return

            # Lag et Discord Embed for å vise resultatene
            embed = discord.Embed(
                title=f"🚍 Reise fra **{fra_sted}** til **{til_sted}**",
                color=discord.Color.blue()
            )

            for idx, trip in enumerate(trips, start=1):
                # Beregn og formater start- og sluttider
                start_time = trip["startTime"][11:16]
                end_time = trip["endTime"][11:16]
                duration = (int(end_time[:2]) * 60 + int(end_time[3:])) - (int(start_time[:2]) * 60 + int(start_time[3:]))

                detaljer = f"🕒 {start_time} – {end_time} ({duration} min)\n"

                # Gå gjennom hvert delstrekning ("leg") i reisen
                for leg in trip["legs"]:
                    # Kartlegg transporttype til passende emoji og navn
                    mode_map = {
                        "Bus": "🚌 Buss",
                        "Rail": "🚆 Tog",
                        "Foot": "🚶 Gå",
                        "Tram": "🚊 Trikk",
                        "Ferry": "⛴️ Ferje",
                        "Metro": "🚇 T-bane"
                    }

                    mode = mode_map.get(leg["mode"].capitalize(), leg["mode"])
                    line = leg["line"]["publicCode"] if leg.get("line") else None
                    from_stop = leg["fromPlace"]["name"]
                    to_stop = leg["toPlace"]["name"]
                    leg_start = trip["startTime"][11:16]
                    leg_end = trip["endTime"][11:16]

                    # Beregn og vis gåavstand hvis delstrekningen er til fots
                    if mode == "🚶 Gå":
                        avstand = self.beregn_avstand(
                            leg["fromPlace"]["latitude"], leg["fromPlace"]["longitude"],
                            leg["toPlace"]["latitude"], leg["toPlace"]["longitude"]
                        )
                        if avstand > 500:
                            detaljer += f"🚶 Gå i {round(avstand / 60)} min ({avstand} meter)\n"
                        continue

                    # Legg til transportinfo med linjenummer hvis tilgjengelig
                    detaljer += (
                        f"{mode} {line} [{leg_start} – {leg_end}]\n" if line
                        else f"{mode} [{leg_start} – {leg_end}]\n"
                    )
                    detaljer += f"• {from_stop} → {to_stop}\n"

                # Legg til hver reise som et eget felt i embed
                embed.add_field(name=f"Alternativ {idx}", value=detaljer, inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.exception("Feil under behandling av kommando")
            await ctx.send("❌ En feil oppstod.")

    async def hent_koordinater(self, sted_navn: str):
        """
        Henter GPS-koordinater for et gitt stedsnavn ved hjelp av Entur sitt geocoder-API.
        Cacher resultatet for å spare API-kall.
        """
        if sted_navn in self.cache:
            return self.cache[sted_navn]

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.entur.io/geocoder/v1/autocomplete",
                params={"text": sted_navn, "size": 1}
            ) as resp:
                data = await resp.json()
                features = data.get("features", [])
                if not features:
                    return None

                coord = features[0]["geometry"]["coordinates"]
                props = features[0]["properties"]
                self.cache[sted_navn] = {
                    "name": props["name"],
                    "lon": coord[0],
                    "lat": coord[1]
                }
                return self.cache[sted_navn]

    def beregn_avstand(self, lat1, lon1, lat2, lon2):
        """
        Beregner avstand i meter mellom to koordinater (lat/lon) med haversine-formelen.
        """
        R = 6371000  # Jordens radius i meter
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return int(R * c)

async def setup(bot):
    """
    Kalles automatisk av Discord-boten når modulen lastes inn.
    Registrerer denne cogen (TravelPlanner) som en del av boten.
    """
    await bot.add_cog(TravelPlanner(bot))
