import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from datetime import datetime
from urllib.parse import urlparse
import logging

class Nyheter(commands.Cog):
    """En cog som håndterer PDF-generering av nettsider."""

    def __init__(self, bot):
        # Referanse til bot-instansen og oppsett av logging
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

    @commands.command(name="pdf")
    async def pdf_command(self, ctx, url: str):
        """
        Discord-kommando for å generere en PDF fra en gitt nettside.
        Bruk: !pdf <url>
        """
        await ctx.send("🔄 Genererer PDF, vennligst vent...")

        try:
            # Generer PDF og send filen i Discord-kanalen
            filename = await self.generate_pdf(url)
            with open(filename, "rb") as f:
                await ctx.send(file=discord.File(f, filename=os.path.basename(filename)))

        except Exception as e:
            # Feilhåndtering og loggføring hvis noe går galt
            await ctx.send(f"🚨 En feil oppstod: {e}")
            self.logger.error(f"Feil under PDF-generering: {e}")

    async def generate_pdf(self, url: str) -> str:
        """
        Bruker Playwright til å besøke en nettside og lagre den som PDF.
        Inkluderer håndtering av cookie-bannere som f.eks. fra vg.no.
        """
        async with async_playwright() as p:
            # Starter en ny, headless nettleser
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()

            self.logger.debug(f"Går til {url}")
            response = await page.goto(url, timeout=60000)  # Timeout etter 60 sekunder

            # Sjekk at siden lastet riktig
            if response and response.status != 200:
                raise Exception(f"Feil ved lasting av nettside (status {response.status})")

            # Forsøk å finne og klikke på cookie-banner (spesielt for vg.no)
            try:
                for frame in page.frames:
                    if "cmp.vg.no" in frame.url:
                        self.logger.debug(f"Fant iframe: {frame.url}")
                        try:
                            # Klikker på "Godta alle"-knappen i cookie-banneret
                            await frame.click("button:has-text('Godta alle')", timeout=5000)
                            self.logger.debug("Klikket på cookie-knappen.")
                        except PlaywrightTimeout:
                            self.logger.warning("Klarte ikke å klikke på cookie-knappen.")
                        break
            except Exception as e:
                self.logger.warning(f"Feil under cookie-håndtering: {e}")

            # Opprett mappe for PDF-filer hvis den ikke finnes
            if not os.path.exists("pdf_filer"):
                os.makedirs("pdf_filer")

            # Genererer et filnavn basert på nettsidens hostname og tidspunkt
            hostname = urlparse(url).hostname or "nyhet"
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"pdf_filer/{hostname}_{timestamp}.pdf"

            # Lagre nettsiden som PDF i A4-format
            await page.pdf(path=filename, format="A4")
            self.logger.debug(f"PDF lagret som {filename}")

            await browser.close()
            return filename

async def setup(bot):
    """Registrerer denne cogen når boten starter."""
    await bot.add_cog(Nyheter(bot))
