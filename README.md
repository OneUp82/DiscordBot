# 🇳🇴 DiscordBot 🇳🇴
*Endelig er den her! Etter månedsvis med hype, rykter og forventninger...*

## 🎉 NORGES BESTE DISCORD BOT ER SLUPPET! 🎉

Har du noen gang drømt om en Discord-bot som faktisk forstår at "vær" ikke betyr "to be" og at "tur" ikke er en turistutflukt? Som ikke spør "did you mean weather?" når du skriver "!vær"? Vel, nå kan du tørke tårene - **DiscordBot** er her for å redde dagen!

### 📢 Hva er DiscordBot?
DiscordBot er en 100% norsk Discord-bot som er designet spesielt for nordmenn som er lei av å måtte snakke engelsk med sine digitale assistenter. Nå kan du endelig sjekke været i Gjøvik, finne bussen fra Røyken til Slemmestad, og spille Postgirobygget - alt sammen på vårt vakre morsmål!

### 🚀 Funksjoner som får selv svenskene til å bli sjalu:

#### 📰 Nyheter / PDF
- **!pdf** – Lei av å klikke på clickbait-artikler? Kommandoen genererer en PDF av en nettside så du kan lagre og lese den i fred og ro.

#### ☁️ Vær
- **!vær** – Sjekk været før du går ut - for du vet aldri når det blir regn i Norge (spoiler: det er alltid regn).

#### 🚌 Reiseplanlegger
- **!tur** – Planlegg turen din mellom to steder. Bruk: `!tur Røyken - Slemmestad`. Perfekt for når Google Maps plutselig bestemmer seg for å sende deg via Stockholm.

#### 🔍 Søkemotorer
- **!google** – Gjør et Google-søk uten å forlate Discord. For når du må bevise for vennene dine at Lofoten faktisk ble stemt fram som verdens vakreste øygruppe.

#### 📅 Ukekommandoer
- **!uke** – For når du har mistet tellinga etter juleferien og ikke vet hvilken uke det er.

#### 🎵 Musikk
- **!yt** – Legg til en sang i spillekøen og start avspilling. Fordi ingenting sier "norsk fest" som Postgirobygget på full guffe.
- **!pause** – Pause musikken når noen trenger å fortelle en "morsom" historie.
- **!fortsett** – Fortsett avspillingen når historien viste seg å ikke være morsom likevel.
- **!skip** – Hopp til neste sang når noen legger på "What Does The Fox Say" for 17. gang.
- **!yt-liste** – Vis nåværende sang og resten av køen (maks 10 sanger vises).
- **!tømkø** – Tøm spillekøen og stopp musikken når festen er over.

#### ℹ️ Hjelp
- **!hjelp** – Viser en oversikt over alle tilgjengelige kommandoer. For de gangene du føler deg hjelpesløs.

## 💻 Installasjon

1. Klon dette repositoriet:
```bash
git clone https://github.com/ditt-brukernavn/discordbot.git
```

2. Installer avhengigheter:
```bash
pip install -r requirements.txt
```

3. Konfigurer bot-token i en `.env`-fil:
```
DISCORD_TOKEN=din_bot_token_her
```

4. Start boten:
```bash
python main.py
```

5. Nyt en helt ny dimensjon av norsk Discord-bruk!

## 📂 Filstruktur

```
discordbot/
├── .env                 # Miljøvariabler (bot token)
├── .gitignore          # Ignorerte filer for git
├── main.py             # Hovedfil for oppstart
├── cookie_handler.py   # Håndtering av cookies for webtjenester
├── requirements.txt    # Liste over nødvendige Python-pakker
├── README.md           # Du leser den nå!
├── commands/
│   ├── commands_help.py # Hjelpkommando
│   ├── google.py        # Google-søk
│   ├── music_player.py  # Musikkavspilling
│   ├── nyheter.py       # Nyheter og PDF-generering
│   ├── travel_planner.py # Reiseplanlegger
│   ├── uke.py           # Ukenummer
│   └── weather.py       # Værkommando
```

## 📜 Lisens

DiscordBoten er distribuert under MIT-lisensen. Det betyr at du kan gjøre hva du vil med koden - akkurat som vi nordmenn liker det! Frihet! Men husk å gi kreditt der det er fortjent, vi er jo tross alt et høflig folk.

## 🤝 Bidrag og forslag

Har du lyst til å gjøre DiscordBoten enda mer norsk? Føl deg fri til å sende inn pull requests eller åpne issues med dine forslag! Vi tar gjerne imot ideer til nye funksjoner og forbedringer. 

### 💡 Ønsker du en ny funksjon?
Åpne en issue med tittelen "Funksjonsforslag: [din idé]" og beskriv hva du ønsker at boten skal kunne gjøre. Vi lover å vurdere alle forslag og implementere de beste etter beste evne! Kanskje det er på tide med:

- Automatiske "God helg!"-meldinger på fredager
- Norsk kalender med røde dager og lokale begivenheter
- En "Hva skjer i [by]"-kommando
- Daglige nyhetsoppdateringer fra norske medier
- Dialekt-oversetter

Ingen forslag er for ville - vi elsker kreative ideer som gjør Discord-opplevelsen mer norsk!

---

*DiscordBot - Fordi selv roboter fortjener å snakke det vakreste språket i verden.* 🇳🇴
