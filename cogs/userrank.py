import discord
import aiohttp
import asyncio
import json
from discord.ext import commands
import requests
from requests.exceptions import HTTPError
import random

quotes = [
    "C4n y0u pwn th4 m4chin3?",
    "Hacker man 0x1 0x0 0x1",
    "The quieter you become the more you are able to hear",
    "\*Morpheus\*: Red or Blue pill?",
    "Access security... Access security grid... YOU DIDN'T SAY THE MAGIC WORD!",
    "Just hack the mainframe.",
    "Z2VsdW5weHpyLnBieg==",
    "The Matrix is real",
    "No place like 127.0.0.1",
    "Hack the planet",
    "Just obfuscate it...",
    "Armitage + Hail Mary",
    "WEP, WPA, WAH?",
    "admin:password",
    "rockyou.txt",
    "tmux > screens",
    "tabs or spaces?",
    "Leeerrrroy Jeekinnnns...",
    "Enumeration is key",
    "Try harder..",
    "https://discord.gg/zGdzUad",
    "Satoshi Nakamoto",
    "Mining Bitcoin...",
    "Configuring neural network"
    ]

def getMoto():
    return quotes[random.randint(0, len(quotes) - 1)]

def getUserImg(username):
    extensions = ["png", "jpg", "jpeg", "gif"]
    retUrl = "https://tryhackme.com/img/THMlogo.png"
    for i in range(0, len(extensions)):
        url = "https://tryhackme.com/uploaded/user_avatars/{}.{}".format(username, extensions[i])
        try:
            response = requests.get(url)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            if "text/html" in response.headers['Content-Type']:
                #print("Not Image")
                pass
            else:
                #print("Probably Image")
                retUrl = url
    return retUrl

def getSubStatus(username):
    url = "https://tryhackme.com/p/{}".format(username)
    check = "No!"
    try:
        response = requests.get(url)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        #print(response.text)
        if "<span>Subscribed</span>" in response.text:
            print("Sub")
            check = "Yes!"
        else:
            print("Not Sub")
            check = "No!"
    return check

def sanitize_check(data):
    chars = ["/",";","-",">","<",":","`","'\""]
    if any((c in chars) for c in data):
        return True
    else:
        return False


class Userrank(commands.Cog,name="Rank Commands"):
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    async def rank(self,ctx,*,user):
        if sanitize_check(user) == True:
            await ctx.send("Sorry, the characters you have entered are blacklisted, instead of trying anything here, try some rooms.")
        else:
            try:
                url = "https://tryhackme.com/api/usersRank/{}".format(user)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as data:
                        data = await data.read()
                        data = json.loads(data)

                        if data.get('userRank') != 0:
                            quip = getMoto()
                            quip = "*{}*".format(quip)
                            response = discord.Embed(title="!rank", description=quip, color=0x148f77)
                            response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
                            userImg = getUserImg(user)
                            response.set_thumbnail(url=userImg)
                            response.add_field(name="Username:", value=user, inline=True)
                            response.add_field(name="Rank:", value=data.get('userRank'), inline=True)
                            sub = getSubStatus(user)
                            response.add_field(name="Subscribed?", value=sub, inline=True)
                            response.set_footer(text="From the TryHackMe Official API!")
                        else:
                            quip = getMoto()
                            quip = "*{}*".format(quip)
                            response = discord.Embed(title="!rank", description=quip, color=0xdc143c)
                            response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
                            userImg = getUserImg(user)
                            response.set_thumbnail(url=userImg)
                            response.add_field(name="Username:", value=user, inline=True)
                            response.add_field(name="Rank:", value="**Error: Username Not Found!**", inline=True)
                            sub = getSubStatus(user)
                            response.add_field(name="Subscribed?", value=sub, inline=True)
                            response.set_footer(text="From the TryHackMe Official API!")
                            
                    await ctx.send(embed=response)
            except:
                await ctx.send("**An issue has occured.**")
        
def setup(bot):
	bot.add_cog(Userrank(bot))
