import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from datetime import datetime
from urllib.parse import urlparse
import logging

class Nyheter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

    @commands.command(name="pdf")
    async def pdf_command(self, ctx, url: str):
        """Genererer en PDF av en nettside og sender den i kanalen."""
        await ctx.send("🔄 Genererer PDF, vennligst vent...")
        try:
            filename = await self.generate_pdf(url)
            with open(filename, "rb") as f:
                await ctx.send(file=discord.File(f, filename=os.path.basename(filename)))
        except Exception as e:
            await ctx.send(f"🚨 En feil oppstod: {e}")
            self.logger.error(f"Feil under PDF-generering: {e}")

    async def generate_pdf(self, url: str) -> str:
        """Åpner nettsiden i en headless nettleser, håndterer cookies og lagrer som PDF."""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()

            self.logger.debug(f"🌐 Går til {url}")
            response = await page.goto(url, timeout=60000)
            
            if response and response.status != 200:
                raise Exception(f"Feil ved lasting av nettside (status {response.status})")

            # Cookie-banner håndtering
            try:
                for frame in page.frames:
                    if "cmp.vg.no" in frame.url:
                        self.logger.debug(f"🔍 Fant iframe: {frame.url}")
                        try:
                            await frame.click("button:has-text('Godta alle')", timeout=5000)
                            self.logger.debug("✅ Klikket på cookie-knappen.")
                        except PlaywrightTimeout:
                            self.logger.warning("⚠️ Klarte ikke å klikke på cookie-knappen.")
                        break
            except Exception as e:
                self.logger.warning(f"⚠️ Feil under cookie-håndtering: {e}")

            if not os.path.exists("pdf_filer"):
                os.makedirs("pdf_filer")

            hostname = urlparse(url).hostname or "nyhet"
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"pdf_filer/{hostname}_{timestamp}.pdf"

            await page.pdf(path=filename, format="A4")
            self.logger.debug(f"📄 PDF lagret som {filename}")

            await browser.close()
            return filename

async def setup(bot):
    await bot.add_cog(Nyheter(bot))
