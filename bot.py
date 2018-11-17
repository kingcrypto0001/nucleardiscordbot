import discord
from discord.ext import commands
import asyncio
import random
import aiohttp
import json
import time
import os
import datetime
nowdatetime = datetime.datetime.now()

tokenfile = "./tokenfile"
TOKEN = tokenfile.read()
VERSION = "v0.0.1"
PREFIX = "-"
OWNERID = ["248242789169496064", "470027393046937620"]
Holidays = [ #1 - Festival Name, #2 - Month, #3 - Day
    ["New Year's Day", 1, 1],
    ["Birthday of Martin Luther King, Jr.", 1, 15],
    ["Washington's Birthday", 2, 19],
    ["Memorial Day", 5, 28],
    ["Independence Day", 7, 4],
    ["Labor Day", 9, 3],
    ["Columbus Day", 10, 8],
    ["Veterans Day", 11, 12],
    ["Thanksgiving Day", 11, 22],
    ["Christmas Day", 12, 25]
]

print("year: %d" % nowdatetime.year)
print("Current month:  %d" % nowdatetime.month)
print("Current day:  %d" % nowdatetime.day)


client = commands.Bot(command_prefix = PREFIX)
client.remove_command("help")


#On Ready Event
@client.event
async def on_ready():
    global SERVERS
    SERVERS = str(len(client.servers))
    global normal_status
    normal_status = VERSION + " | " + PREFIX + "help | Servers: " + SERVERS
    print(normal_status)
    await client.change_presence(game = discord.Game(name = normal_status))
    print("Bot Connected.")

#On Message Event
@client.event
async def on_message(message):
    try:
        message.content = message.content.lower()
        await client.process_commands(message)
    except: discord.ext.commands.CommandNotFound

#Next Holiday Command
@client.command(pass_context = True)
async def nextholiday(ctx):
    nh = ""

    await client.say(nh)

#All Holidays Command
@client.command(pass_context = True)
async def ahs(ctx):
    embed = discord.Embed(title = "Holidays 2018!", color = discord.Colour.blue())

    for h in Holidays:
        embed.add_field(name = h[0], value = str(h[1]) + "/" + str(h[2]) + " - in {} day/s".format("12"), inline = False)

    await client.say(embed = embed)

#Invite Link Command
@client.command(pass_context = True)
async def botinvite(ctx):
    await client.say("https://discordapp.com/api/oauth2/authorize?client_id=498698783320834069&permissions=8&scope=bot")


#Clear Command
@client.command(pass_context = True)
async def clear(ctx, amount):
    await client.delete_message(ctx.message)
    channel = ctx.message.channel
    amount = int(amount)
    messages = []
    async for message in client.logs_from(channel, limit = amount):
        if amount > 100:
            await client.delete_message(message)
            await asyncio.sleep(0.05)
        elif amount <= 100:
            messages.append(message)

    try:
        await client.delete_messages(messages)
    except:
        discord.errors.NotFound, discord.errors.ClientException, discord.ext.commands.errors.CommandInvokeError

#MemberCount Command
@client.command(pass_context = True)
async def membercount(ctx):
    embed = discord.Embed(colour = discord.Colour.blue())
    embed.set_author(name = str(ctx.message.server.member_count) + " members")
    await client.say(embed = embed)

#Change Status Command
@client.command(pass_context = True)
async def status(ctx, *args):
    for ownerid in OWNERID:
        if ctx.message.author.id == ownerid:
            output = ""
            for word in args:
                output = output + word
                output = output + " "

            if output == "(normal) ":
                await client.change_presence(game = discord.Game(name = normal_status))
                m = await client.say("Status was changed to " + normal_status)
                await asyncio.sleep(4)
                await client.delete_message(m)
            else:
                await client.change_presence(game = discord.Game(name = output))
                m = await client.say("Status was changed to " + output)
                await asyncio.sleep(4)
                await client.delete_message(m)
        else:
            try:
                await client.delete_message(ctx.message)

            except: discord.errors.NotFound, discord.errors.ClientException, discord.ext.commands.errors.CommandInvokeError

#Bitcoin Bot Command
@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        embed = discord.Embed(color = discord.Colour.blue())
        embed.set_author(name = "Bitcoin price is: $" + response["bpi"]["USD"]["rate"] + " | Last Updated: " + response["time"]["updated"])
        await client.say(embed = embed)

#Echo Bot Command
@client.command(pass_context = True)
async def echo(ctx, *args):
    print(ctx.message.content + " - " + str(ctx.message.author))
    await client.delete_message(ctx.message)
    output = ""
    for word in args:
        output = output + word
        output = output + " "

    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name = output)

    await client.say(embed = embed)

#Dm Command
@client.command(pass_context = True)
async def dm(ctx, user : discord.Member, c : discord.Colour, *args): # : discord.Member
    if ctx.message.author == ctx.message.channel.server.owner:
        output = ""
        for word in args:
            output = output + word
            output = output + " "


        embed = discord.Embed(title = output, colour = c)

        await client.send_message(user, embed = embed)
        success_M = await client.say("Message successfully sent to {}.".format(user))
        await asyncio.sleep(4)
        await client.delete_message(ctx.message)
        await client.delete_message(success_M)
    else:
        for ownerid in OWNERID:
            if ctx.message.author.id == ownerid:
                output = ""
                for word in args:
                    output = output + word
                    output = output + " "


                embed = discord.Embed(title = output, colour = c)

                await client.send_message(user, embed = embed)
                success_M = await client.say("Message successfully sent to {}.".format(user))
                await asyncio.sleep(4)
                await client.delete_message(ctx.message)
                await client.delete_message(success_M)

            else:
                m = await client.say('The "dm" command is only for the server owner.')
                await asyncio.sleep(4)
                await client.delete_message(m)
                await client.delete_message(ctx.message)

#Dm with ID Command
@client.command(pass_context = True)
async def dmu(ctx, id, c : discord.Colour, *args): # : discord.Member
        user = await client.get_user_info(id)
        output = ""
        for word in args:
            output = output + word
            output = output + " "


        embed = discord.Embed(title = output, colour = c)

        await client.send_message(user, embed = embed)
        success_M = await client.say("Message successfully sent to {}.".format(user))
        await asyncio.sleep(4)
        await client.delete_message(ctx.message)
        await client.delete_message(success_M)

#Ping Bot Command
@client.command(pass_context = True)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await client.send_typing(channel)
    t2 = time.perf_counter()
    embed=discord.Embed(title = "Ping: {}".format(round((t2-t1)*1000)), colour = discord.Colour.blue())
    await client.say(embed=embed)

#Flipcoin Bot Command
@client.command(pass_context = True)
async def flipcoin(ctx):
    answer = random.choice(["Heads!", "Tails!"])
    embed = discord.Embed(title = answer, colour = discord.Colour.blue())

    await client.say(embed = embed)
#Restart Bot Command
@client.command()
async def restart():
    await client.say("Restarting bot...")
    await client.close()

#Help Command
@client.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        title = "Prefix: " + PREFIX,
        colour = discord.Colour.blue()
    )

    embed.set_author(name = "HELP")

    embed.add_field(name = "clear", value = "Clears the amount of messages [arg1]. You can only delete more then 2 messages.", inline = False)
    embed.add_field(name = "bitcoin", value = "Shows 1 BTC amount in USD.", inline = False)
    embed.add_field(name = "flipcoin", value = "Flips a coin for you!", inline = False)
    embed.add_field(name = "dm", value = "Dms a user for you (SERVER-OWNER ONLY). [arg1]-User, [arg2]-Color, [arg3]-Message")

    await client.say(embed = embed)


#Command Error Handler
#@client.event
#async def on_command_error(error, ctx):
#    if isinstance(error, commands.CommandNotFound):
#        await client.send_message(ctx.message.channel, "Invalid Command. {}".format(ctx.message.author.mention))
#        return




































#Run bot
client.run(TOKEN)
