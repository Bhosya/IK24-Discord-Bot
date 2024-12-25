import asyncio
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os

# Load token dari file .env
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Inisialisasi intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# Inisialisasi bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Ketika bot siap
@bot.event
async def on_ready():
    print(f"[INFO] Bot telah siap!")
    print(f"[INFO] Login sebagai: {bot.user} (ID: {bot.user.id})")
    print(f"[INFO] Terhubung ke {len(bot.guilds)} server.")

# Fungsi utama untuk memulai bot
async def main():
    async with bot:
        try:
            print("[INFO] Memuat extension 'scraper_cog'...")
            await bot.load_extension("cogs.scraper_cog")
            print("[INFO] Extension 'scraper_cog' berhasil dimuat.")
        except Exception as e:
            print(f"[ERROR] Gagal memuat extension 'scraper_cog': {e}")

        # Jalankan bot
        try:
            print("[INFO] Bot sedang dijalankan...")
            await bot.start(TOKEN)
        except Exception as e:
            print(f"[ERROR] Bot gagal dijalankan: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO] Bot dihentikan oleh pengguna.")
    except Exception as e:
        print(f"[ERROR] Bot dihentikan karena error: {e}")