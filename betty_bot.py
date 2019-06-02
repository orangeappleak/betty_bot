import discord
import discord.channel
from discord.ext import commands
import random
import os

extensions = ['mysql','errors','wikipedia','face_recog']
client = commands.Bot("#")

@client.command(aliases = ['hi','hey','wassup','how you doing'])
async def hello(ctx):
    channel=ctx.message.channel
    await channel.send("wassup dawg")

@client.command()
async def relation(ctx):
    channel=ctx.message.channel
    await channel.send("i am just a bot,and now you want to talk about relations and all ")

@client.event
async def on_ready():
    print("Working as {}".format(client.user.name))

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded due to,[{}]'.format(extension,error))

    client.run(os.environ.get('TOKEn'))
