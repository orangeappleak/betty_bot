import discord
from discord.ext import commands

class errors(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        ignored = (commands.CommandNotFound,commands.UserInputError)
        error = getattr(error,'original',error)

        if isinstance(error,ignored):
            embed=discord.Embed(title="ERROR FOUND",color=0xff0000)
            embed.add_field(name='error_description->',value=error,inline=False)
            embed.set_author(name=ctx.message.author,icon_url=ctx.message.author.avatar_url)
            embed.set_footer(text='TYPE IN #HELP FOR MORE INFO ON COMMANDS')
            await ctx.message.channel.send(embed=embed)

    @commands.command()
    async def ping(self,ctx):
        await ctx.message.channel.send("pong")

def setup(client):
    client.add_cog(errors(client))

