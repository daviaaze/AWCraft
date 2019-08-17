import discord
import aws
import json

from discord.ext import commands

config_file =open('config.json', 'r+')

data = json.load(config_file)
    
credentials = data['credentials']

modes = data['modes']

bot = commands.Bot(command_prefix='?')

curMode = ""

# bot commands
@bot.command()
async def start(ctx, mode):
    aws.start(mode)
    curMode = mode
    await ctx.send(mode + "server is starting")
    

@bot.command()
async def mode(ctx, sub, mode):
    if sub == 'add':
        data['modes'].append(mode)
        config_file.seek(0)
        json.dump(data, config_file)
        config_file.truncate()
    if sub == 'remove':
        data['modes'].remove(mode)
        config_file.seek(0)
        json.dump(data, config_file)
        config_file.truncate()
    if sub == 'list':
        await ctx.send("Available modes: {}".format(data['modes']))

@bot.command()
async def stop(ctx):
    aws.stop()
    ctx.send("Server is Stopping")
    curMode = ''


@bot.command()
async def restart(ctx, mode=curMode):
    aws.restart()
    if mode != '':
        curMode = mode
    await ctx.send("Server is restarting in mode {}".format(mode))
    

@bot.command()
async def status(ctx):  
    await ctx.send("Server is: " + aws.status())


bot.remove_command('help')


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="AWS + Minecraft Bot", description="Commands:", color=0xeee657)
    
    embed.add_field(
        name="?status", value="Shows the status of the instance", inline=False)
    embed.add_field(
        name="?start", value="Start the server, use !start ""mode""\n modes: {}".format(data['modes'], inline=False))
    embed.add_field(
        name="?stop", value="Turn off server", inline=False)
    embed.add_field(
        name="?restart", value="Restart the server, use !restart mode\n modes:\n\tvanilla\n\ttekkit", inline=False)
    embed.add_field(name="!help", value="Gives this message", inline=False)
    embed.add_field(
        name="?mode", value="with modes you can:\n\t?mode add: add a mode\n\t?mode remove:Remove a mode\n\t?mode list: See availeable modes", inline=False)
    
    await ctx.send(embed=embed)

bot.run(credentials["discord"])
