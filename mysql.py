import discord
from discord.ext import commands
import aiomysql
import asyncio

loop = asyncio.get_event_loop()

class mysql(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def register(self,ctx):
        try:
            conn=await aiomysql.connect(host=127.0.0.1,user="root",password="karthik.123",db="discord")
            async with conn.cursor() as curr:
                user = str(ctx.message.author)
                id=user.split("#")
                sql="insert into clients (user_name,user_id) values(%s,%s)"
                val=(id[0],id[1])
                await curr.execute("select user_id from clients")
                records=await curr.fetchall()
                count=0
                for record in records:
                    if int(id[1])==record[0]:
                        count=count+1
                        break
                if count>=1:
                    await ctx.message.channel.send("sorry,but you are already registered with database")
                else:
                    await curr.execute(sql,val)
                    await conn.commit()
                    conn.close()
                    await ctx.message.channel.send("registering......")
                    await asyncio.sleep(4)
                    await ctx.message.channel.send("you are now successfully registered with the database")
        except Exception as error:
            print(error)

def setup(client):
    client.add_cog(mysql(client))
