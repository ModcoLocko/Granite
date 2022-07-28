import requests
import json
import discord
from discord.ext import commands
from mcstatus import JavaServer
import base64

with open("token.txt") as token:
	TOKEN = token.read()



bot = commands.Bot(command_prefix='/')

@bot.command()
async def mod(ctx, arg):
    response = ((requests.get(f'https://api.modrinth.com/v2/search?limit=1&query={arg}')).json())
    try:
        response = ((response["hits"])[0])
    except:
        embed=discord.Embed(description="No Results Found", color=0xa51d2d)
        await ctx.send(embed=embed)
    title, author, desc, slug, img = (response["title"]), (response["author"]), (response["description"]), (response["slug"]), (response["icon_url"])
    url = (f"https://modrinth.com/mod/{slug}")
    embed=discord.Embed(title=title, url=url, description=desc, color=0x57e389)
    embed.set_author(name=author)
    embed.set_thumbnail(url=img)
    await ctx.send(embed=embed)

@bot.command()
async def mango(message):
    await message.author.send(":mango:")

@bot.command()
async def serverinfo(ctx, arg):
    try:
        server = JavaServer.lookup(arg)
        status = server.status()
    except:
        embed=discord.Embed(description="Could not Locate Server", color=0xa51d2d)
        await ctx.send(embed=embed)
    latency = int(status.latency)
    embed=discord.Embed(title="The server is online", description=f"The server has {status.players.online} players and replied in {latency} ms", color=0x8ff0a4)
    await ctx.send(embed=embed)

@bot.command()
async def skin(ctx, arg):
    try:
        response = ((requests.get(f'https://api.mojang.com/users/profiles/minecraft/{arg}')).json())
        response = (response.json())
        uuid = (response["id"])
        data = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}')
        data = (data.json())
        prop = (data["properties"])
        one = (prop[0])
        basemsg = (one["value"])
        decodedBytes = base64.b64decode(basemsg)
        decodedStr = str(decodedBytes, "utf-8")
        skindatadict = json.loads(decodedStr)
        skinimage = (((skindatadict["textures"])["SKIN"])["url"])
        name = (skindatadict["profileName"])
        embed=discord.Embed(title=name, color=0xc061cb)
        embed.set_thumbnail(url=skinimage)
        await ctx.send(embed=embed)
    except:
        embed=discord.Embed(description="Could not Locate Skin", color=0xa51d2d)
        await ctx.send(embed=embed)



bot.run(TOKEN)
