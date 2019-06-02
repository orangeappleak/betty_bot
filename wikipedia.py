import discord
from discord.ext import commands
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup

class wikipedia(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command(pass_context=True)
    async def wiki(self,ctx):
        try:
            await ctx.message.channel.send("channeling information from wikipedia..........")
            content=str(ctx.message.content).split(" ")
            search=[]
            for s in content[1:]:
                print("s:",s)
                search.append(s.capitalize())
            print("search",search)
            search_string='_'.join(search[0:])
            print("search_string:",search_string)
            website=requests.get('https://en.wikipedia.org/wiki/{}'.format(search_string)).text
            url='https://en.wikipedia.org/wiki/{}'.format(search_string)
            soup=BeautifulSoup(website,'lxml')
            heading=soup.find('h1',attrs={'id':'firstHeading'}).text
            body=soup.find('div',class_="mw-body").find('div',class_="mw-body-content",attrs={'id':'bodyContent'}).find('div',class_="mw-content-ltr",attrs={'id':'mw-content-text'}).find('div',class_="mw-parser-output")
            paras=body.find_all('p')
            no_of_paras=len(paras)
            lists=body.find_all('ul')
            embed=discord.Embed(title=heading,description="BE MORE SPECIFIC",color=0x4286f4)
            embed.set_image(url='https://cdn.arstechnica.net/wp-content/uploads/2015/09/2000px-Wikipedia-logo-v2-en-640x735.jpg')
            embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            if(no_of_paras<=2):
                for p in paras[0:4]:
                    try:
                        p=p.text
                    except Exception as error:
                        continue
                embed.add_field(name="LISTS FOUND:",value=lists[0].text,inline=False)
                embed.add_field(name="FOR MORE INFO,VISIT:",value='https://en.wikipedia.org/wiki/{}'.format(search_string),inline=True)
                embed.set_footer(text="SOURCE OF INFORMATION:Wikipedia({})".format('https://www.wikipedia.org/'))
                await ctx.message.channel.send(embed=embed)
            else:
                for p1 in paras[0:3]:
                    try:
                        para_embed=discord.Embed(title=heading,description="number of paragraphs found:{}".format(no_of_paras),color=0x4346f5)
                        para_embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
                        para_embed.set_thumbnail(url='https://cdn.arstechnica.net/wp-content/uploads/2015/09/2000px-Wikipedia-logo-v2-en-640x735.jpg')
                        para_embed.add_field(name="INFORMATION ABOUT:{}".format(heading),value=p1.text,inline=False)
                        para_embed.set_footer(text="SOURCE OF INFORMATION:Wikipedia({})".format('https://www.wikipedia.org/'))
                        await ctx.message.channel.send(embed=para_embed)
                    except Exception as error:
                        continue
                para_embed.clear_fields()
                para_embed.add_field(name="FOR MORE INFO,VISIT:",value='https://en.wikipedia.org/wiki/{}'.format(search_string),inline=True)
                await ctx.message.channel.send(embed=para_embed)

        except Exception as error:
            try:
                search_str='+'.join(search[1:])
                err_page=requests.get('https://en.wikipedia.org/w/index.php?search={}&title=Special%3ASearch&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1'.format(search_str)).text
                soup1=BeautifulSoup(err_page,'lxml')
                err=soup1.find('div',class_="mw-body").find('div',class_="mw-body-content",attrs={'id':'bodyContent'}).find('div',attrs={'id':'mw-content-text'}).find('div',class_="searchresults")
                error_embed=discord.Embed(title="PAGE NOT FOUND",color=0xff0000)
                error_embed.set_thumbnail(url='https://cdn.arstechnica.net/wp-content/uploads/2015/09/2000px-Wikipedia-logo-v2-en-640x735.jpg')
                error_embed.add_field(name="description",value=err.p.text)
                error_embed.add_field(name="FOR MORE INFO,VISIT:",value='https://en.wikipedia.org/wiki/{}'.format(search_string),inline=True)
                error_embed.set_footer(text="SOURCE OF INFORMATION:Wikipedia({})".format('https://www.wikipedia.org/'))
                try:
                    suggestions=discord.Embed(title="consider these suggestions",color=0x20c90a)
                    suggestions.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
                    suggest=err.ul.find_all('a')
                    i=0
                    for s in suggest[0:10]:
                        suggestions.add_field(name="SUGGESTION {}:".format(i+1),value=s.text,inline=False)
                        i=i+1
                    await ctx.message.channel.send(embed=error_embed)
                    await ctx.message.channel.send(embed=suggestions)
                except Exception as error:
                    await ctx.message.channel.send(embed=error_embed)
            except Exception as e:
                print(e)
def setup(client):
    client.add_cog(wikipedia(client))
