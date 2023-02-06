import discord
import json
import os
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command


def get_directories(path):
    dirs = []
    while True:
        path, directory = os.path.split(path)
        if directory != "":
            dirs.append(directory)
        else:
            if path != "":
                dirs.append(path)
            break
    return dirs[::-1]


class room(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    room = discord.SlashCommandGroup(
        "room",
        "控制跨群聊天房間",
        guild_only=True,
        default_member_permissions=discord.Permissions(8))

    @room.command(description="創建一個跨群聊天室")
    async def create(self, ctx, name: Option(str, "要創建聊天室的代碼")):
        # 檢查名稱是否符合規則
        if all(c.isalnum() for c in name) == False:
            return await ctx.respond("房間必須是字母與數字")

        if name in get_directories("data/room"):
            return await ctx.respond("我的天這名字被搶了")

        userpath = F"data/user/{ctx.author.id}.json"
        # 檢查用戶檔案是否存在
        if not os.path.isfile(userpath):
            with open(userpath, "w") as file:
                data = {
                    "limit": {
                        "now": 0,
                        "mix": 1
                    },
                    "room": []
                }
                json.dump(data, file, indent=4)
        # 用戶檔案更新
        with open(userpath, "r") as file:
            data = json.load(file)
            # 檢測創建上限
            if data["limit"]["now"] >= data["limit"]["mix"]:
                return await ctx.respond("你只有權限創建一個聊天室")
            # 更新資料
            data["room"].append(name)
            data["limit"]["now"] += 1
        # 上傳資料
        with open(userpath, "w") as file:
            json.dump(data, file, indent=4)

        # 創建room資料夾
        roompath = F"data/room/{name}"
        os.makedirs(roompath)
        # info
        with open(F"{roompath}/info.json", "w") as file:
            data = {"owner": ctx.author.id, "pubilc": True}
            json.dump(data, file, indent=4)
        # guilds
        with open(F"{roompath}/guild.json", "w") as file:
            data = {}
            json.dump(data, file, indent=4)
        # bans
        with open(F"{roompath}/ban.json", "w") as file:
            data = []
            json.dump(data, file, indent=4)

        embed = discord.Embed(
            title="成功創建跨群聊天室", description=F"/join [{name}] [channel]")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(room(bot))
