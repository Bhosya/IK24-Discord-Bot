import asyncio
import discord
from discord.ext import commands, tasks
from utils.elnino_scraper import login_to_moodle, check_new_tasks

CLASS_MAPPING = {
    "IK-A": {
        "channel": 1320430074721206312,
        "username": "3.34.24.0.26",
        "password": "Polines*2024",
        "file": "elnino_tasks_ik_a.json",
        "matkul": {
            "Desain Grafis dan Multimedia": "https://elnino20212.polines.ac.id/course/view.php?id=7101",
            "Pengantar Teknologi Informasi": "https://elnino20212.polines.ac.id/course/view.php?id=7119",
            "Sistem Basis Data": "https://elnino20212.polines.ac.id/course/view.php?id=7103",
            "Sistem Operasi": "https://elnino20212.polines.ac.id/course/view.php?id=7102"
        }
    },
    "IK-B": {
        "channel": 1320435722892607539,
        "username": "3.34.24.1.23",
        "password": "Polines*2024",
        "file": "elnino_tasks_ik_b.json",
        "matkul": {
            "Algoritma dan Pemrograman": "https://elnino20212.polines.ac.id/course/view.php?id=7116",
            "Desain Grafis dan Multimedia": "https://elnino20212.polines.ac.id/course/view.php?id=7130",
            "Pengantar Teknologi Informasi": "https://elnino20212.polines.ac.id/course/view.php?id=7145",
            "Sistem Basis Data": "https://elnino20212.polines.ac.id/course/view.php?id=7132",
            "Sistem Operasi": "https://elnino20212.polines.ac.id/course/view.php?id=7131"
        }
    },
    "IK-C": {
        "channel": 1320435752169111686,
        "username": "3.34.24.2.01",
        "password": "Polines*2024",
        "file": "elnino_tasks_ik_c.json",
        "matkul": {
            "Desain Grafis dan Multimedia": "https://elnino20212.polines.ac.id/course/view.php?id=7150",
            "Pengantar Teknologi Informasi": "https://elnino20212.polines.ac.id/course/view.php?id=7383",
            "Sistem Basis Data": "https://elnino20212.polines.ac.id/course/view.php?id=7152",
            "Sistem Operasi": "https://elnino20212.polines.ac.id/course/view.php?id=7151"
        }
    },
    "IK-D": {
        "channel": 1320435775103303791,
        "username": "3.34.24.3.05",
        "password": "Lupasandi28!",
        "file": "elnino_tasks_ik_d.json",
        "matkul": {
            "Desain Grafis dan Multimedia": "https://elnino20212.polines.ac.id/course/view.php?id=7165",
            "Algoritma dan Pemrograman": "https://elnino20212.polines.ac.id/course/view.php?id=7142",
            "Sistem Basis Data": "https://elnino20212.polines.ac.id/course/view.php?id=7167",
            "Sistem Operasi": "https://elnino20212.polines.ac.id/course/view.php?id=7166"
        }
    },
    # "ik-e": {
    #     "channel": 1320435797354086420,
    #     "username": "--username--",
    #     "password": "Polines*2024",
    #     "file": "elnino_tasks_ik_e.json",
    #     "matkul": {
    #         "Algoritma Pemrograman": "--link--",
    #         "Algoritma Pemrograman": "--link--",
    #     }
    # }
}

class ScraperCog(commands.Cog):
    """Cog untuk memantau tugas baru dari setiap kelas di Elnino."""

    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}  # Sesi login untuk setiap kelas
        self.check_tasks.start()

    def cog_unload(self):
        self.check_tasks.cancel()

    @tasks.loop(minutes=5)
    async def check_tasks(self):
        for class_name, config in CLASS_MAPPING.items():
            # Login jika belum ada sesi
            if class_name not in self.sessions:
                session = login_to_moodle(config["username"], config["password"])
                if session:
                    self.sessions[class_name] = session
                else:
                    print(f"[ERROR] Login gagal untuk {class_name}.")
                    continue

            session = self.sessions[class_name]
            file_path = config["file"]
            channel_id = config["channel"]

            for matkul_name, matkul_url in config["matkul"].items():
                new_tasks = check_new_tasks(session, matkul_url, matkul_name, file_path)

                if new_tasks:
                    channel = self.bot.get_channel(channel_id)
                    if channel:
                        for task in new_tasks:
                            guild = self.bot.get_guild(channel.guild.id)  # Ambil guild berdasarkan ID channel
                            role = discord.utils.get(guild.roles, name=class_name)  # Cari role berdasarkan nama kelas
                            if role:
                                await channel.send(
                                    f"-----------------------------------------------------------------------\n\n"
                                    f"🔔 **Tugas Baru!** {role.mention}\n"
                                    f"**{task['name']}** ({task['course']})\n"
                                    f"📎 {task['url']}"
                                )
                            else:
                                await channel.send(
                                    f"🔔 **Tugas Baru!** (Role {class_name} tidak ditemukan)\n"
                                    f"**{task['name']}** ({task['course']})\n"
                                    f"📎 {task['url']}"
                                )


    @check_tasks.before_loop
    async def before_check_tasks(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(ScraperCog(bot))
