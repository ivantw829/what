import json
import os
import discord
from discord.ext import commands

bot = commands.Bot(help_command=None, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f">>{bot.user}上線<<")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'✅   已加載 {filename}')
        except Exception as error:
            print(f'❎   {filename} 發生錯誤  {error}')

with open("config.json", "r", encoding="UTF-8") as file:
    data = json.load(file)
bot.run(data["token"])
