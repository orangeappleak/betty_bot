import discord
import discord.channel
from discord.ext import commands
import random
import os

extensions = ['errors','wikipedia']
client = commands.Bot("#")
client.remove_command('help')

@client.command(aliases = ['hi','hey','wassup','how you doing'])
async def hello(ctx):
    channel=ctx.message.channel
    await channel.send("wassup dawg")
    
@client.command(pass_context=True)#custom help command
async def help(ctx):
    try:
        help_embed=discord.Embed(title="List of commands that the bot can perform",color=0x00ff19)
        help_embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        help_embed.set_thumbnail(url=ctx.message.author.avatar_url)
        help_embed.add_field(name="hello->",value="Greets the user back")
        help_embed.add_field(name="wiki [search string]->",value="extracts data from wikipedia based on the entered search string")
        help_embed.add_field(name="register->",value="registers the author's name into the database")
        help_embed.add_field(name="(admin_command) create_channel [name][type]->",value="creates a text or a voice channel based on the given parameters")
        help_embed.add_field(name="profile [user_name]->",value="provides information based on the given user_name")
        help_embed.add_field(name="permissions [role]->",value="gives the list of permissions for the specified role")
        help_embed.add_field(name="roles->",value="lists all the roles for the server")
        help_embed.add_field(name="role [user_name]->",value="lists the roles assigned to the user_name")
        help_embed.add_field(name="(admin_command) kick [member]->",value="kicks the specified user from the server")
        help_embed.add_field(name="(admin_command) delete_messages->",value="deletes 100 recent messages from the channel")
        help_embed.set_footer(text="NOTE->DONT FORGET TO ADD THE BOT_PREFIX[#] BEFORE THE COMMAND")
        await ctx.message.channel.send(embed=help_embed)
    except Exception as error:
        print(error)
 
@client.command()
async def running(ctx):
    await ctx.message.channel.send("running 24/7 on heroku")
   
@client.command()
async def profile(ctx,member:discord.Member):
    try:
        r=[]
        for role in member.roles:
            r.append(role.name)
        iembed=discord.Embed(title="Info for the user:{}".format(member.name))
        iembed.add_field(name="User_name->",value=member.name)
        iembed.add_field(name="User_id->",value=member.id)
        iembed.add_field(name="User_status->",value=member.status)
        for i in range(len(r)):
            iembed.add_field(name="User_role:%s->" % str(i+1),value=r[i],inline=False)
        iembed.add_field(name="Member of the server from->",value=member.joined_at)
        iembed.set_author(name=member.name,icon_url=member.avatar_url)
        iembed.set_thumbnail(url=member.avatar_url)
        await ctx.message.channel.send(embed=iembed)
    except Excetpion as error:
        print(error)
        
@client.command(pass_context=True)
async def create_channel(ctx,name,type):
    try:
        if 'admin' in (role.name for role in ctx.message.author.roles):
            if type == 'text':
                await ctx.message.channel.category.guild.create_text_channel(name=name)
                await ctx.message.channel.send("The text channel named {} has been created successfully".format(name))
            elif type == 'voice':
                await ctx.message.channel.category.guild.create_voice_channel(name=name)
                await ctx.message.channel.send("The voice channel named {} has been created successfully".format(name))
        else:
            await ctx.message.channel.send("```you do not have the right permissions to execute that command```")
    except Exception as error:
        print(error)
 
@client.command(pass_context=True)
async def permissions(ctx,role:discord.Role):
    permission_embed=discord.Embed(title="the current permissions for {} are:".format(role.name),color=discord.Colour.orange())
    for permission in role.permissions:
        permission_embed.add_field(name=permission[0],value=permission[1])
    await ctx.message.channel.send(embed=permission_embed)

@client.command(pass_context=True)
async def roles(ctx):
    try:
        roles_embed=discord.Embed(title="The current roles in the server are:",color=discord.Colour.blue())
        for role in ctx.message.author.guild.roles:
            roles_embed.add_field(name="role_name:",value=role.name,inline=True)
        await ctx.message.channel.send(embed=roles_embed)
    except Exception as error:
        print(error)

@client.command(pass_context=True)
async def role(ctx,member:discord.Member):
    try:
        role_embed=discord.Embed(title="The current roles for {} in the server are:".format(member.name),color=discord.Colour.green())
        for role in member.roles:
            role_embed.add_field(name="role:",value=role.name,inline=True)
        await ctx.message.channel.send(embed=role_embed)
    except Exception as error:
        print(error)

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx,member: discord.Member):
    try:
        if 'admin' in (role.name for role in ctx.message.author.roles):
            if member == client.user:
                await ctx.message.channel.send("```kicking betty_bot is not possible```")
            else:
                await ctx.message.channel.send("kicking {}".format(member))
                await client.kick(member)
        else:
            await ctx.message.channel.send("```you need to be an admin in order to do that```")
    except Exception as error:
        embed=discord.Embed(title="ERROR FOUND",color=0xff0000)
        embed.add_field(name='error_description->',value=error,inline=False)
        embed.set_author(name=ctx.message.author,icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text='TYPE IN #HELP FOR MORE INFO ON COMMANDS')
        await ctx.message.channel.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def delete_messages(ctx):
    try:
        if 'admin' in (role.name for role in ctx.message.author.roles):
            await ctx.message.channel.send("gimme a sec")
            deleted_messages=await ctx.message.channel.purge()
            await ctx.message.channel.send("There you go MR.<@%s>" % ctx.message.author.id)
        else:
            await ctx.message.channel.send("```you do not have the right permission to do that```")
    except Exception as error:
        print(error)

@client.command()
async def relation(ctx):
    channel=ctx.message.channel
    await channel.send("i am just a bot,and now you want to talk about relations and all ")

@client.event
async def on_ready():
    game=discord.Game("running on heroku")
    await client.change_presence(status=discord.Status.online,activity=game)
    print("Working as {}".format(client.user.name))
    
if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded due to,[{}]'.format(extension,error))

    client.run(os.environ.get('TOKEN'))
