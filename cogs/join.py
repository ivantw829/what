import discord
import json
import os
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command

class join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="加入一個跨群聊天")
    async def join(self, ctx,
                   room: Option(str, "要加入的房間代碼"),
                   channel: Option(discord.TextChannel, "要跨群聊天的頻道")):
        await ctx.defer() #推遲回應

        # 檢查聊天室是否存在
        roompath = F"data/room/{room}"
        if not os.path.isdir(roompath):
            return await ctx.respond("沒有這個聊天室")

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("需要`管理員權限`才能加入跨群聊天室")

        # 讀取聊天室檔案
        with open(F"{room}/info.json","r") as file:
            data = json.load(file)

            # 檢查是否為公開群組
            if data["pubilc"] == False:
                if not ctx.author.id == data["owner"]:
                    return await ctx.respond("非公開聊天室只能由擁有者加入")
        
        # 更新該聊天室的參與群統計
        with open(F"{room}/guild.json","r") as file:
            data = json.load(file)
            data[str(ctx.guild.id)] = channel.id
        with open(F"{room}/guild.json","w") as file:
            json.dump(data,file)

        guildpath = F"data/guild/{ctx.guild.id}.json" #群組設置檔案
        #檢查群組是否有設置檔
        if not os.path.isfile(guildpath):
            with open(guildpath,"w") as file:
                data = {}
                json.dump(data,file,indent=4)
        #更改群組資訊
        with open(guildpath,"r") as file:
            data=json.load(file)
            data[str(channel.id)] = room
        with open(guildpath,"w") as file:
            json.dump(data,file)

        #發送回應
        embed=discord.Embed(description=F"成功在{channel.mention}加入`{room}`")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(join(bot))
