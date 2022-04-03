from cgitb import text
import datetime
from multiprocessing.sharedctypes import Value
from sqlite3 import Timestamp
from unicodedata import name
import discord
from discord import Embed
from discord.ext import commands
import youtube_dl

client = commands.Bot(command_prefix='!')

# TODO
# refactor all of the embeds to reduce rededuancy

@client.event
async def on_ready():
    print('beep boop....')

@client.command()
async def play(ctx, url : str):
    embed = Embed(timestamp = datetime.datetime.utcnow())
    embed.set_author(name = 'moosiqa bot', icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFNH7o1opnSCS_88e-bfYSYr_mnCas2zVUwA&usqp=CAU')
    
    if ctx.author.voice is None:
        embed.add_field(name='Join Voice Chat', value='You need to join a voice chat.', inline=False)
        await ctx.send(embed=embed)

    voice_channel = ctx.author.voice.channel      
    voice = discord.utils.get(client.voice_clients)
    print(f'Voice Channel: {voice_channel}\bVoice:{voice}')
    
    if voice is None:
        await voice_channel.connect()
    
    ffmpeg_options = {
        'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        , 'options':'-vn'
    }

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        voice = discord.utils.get(client.voice_clients)
        info = ydl.extract_info(url, download = False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2,**ffmpeg_options)
        print(info['title'])

        embed.add_field(name='Playing', value=info['title'], inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}')
        await ctx.send(embed=embed)
        
        voice.play(source)

@client.command()
async def leave(ctx):
    embed = Embed(timestamp = datetime.datetime.utcnow())
    embed.set_author(name='moosiqa bot', icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFNH7o1opnSCS_88e-bfYSYr_mnCas2zVUwA&usqp=CAU')
    
    voice = discord.utils.get(client.voice_clients)
    if voice.is_connected():
        embed.add_field(name='Good Bye', value='See ya later', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}')
        await ctx.send(embed=embed)
        await voice.disconnect()
    else:
        embed.add_field(name='Not in Channel', value='Not in Channel', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}')
        await ctx.send(embed=embed)

@client.command()
async def pause(ctx):

    embed = Embed(timestamp = datetime.datetime.utcnow())
    embed.set_author(name='moosiqa bot', icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFNH7o1opnSCS_88e-bfYSYr_mnCas2zVUwA&usqp=CAU')
    
    voice = discord.utils.get(client.voice_clients)
    if voice.is_playing():
        embed.add_field(name='Pausing', value='Holding my breath', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}')
        await ctx.send(embed=embed)
        voice.pause()
    else:
        embed.add_field(name='Already Pause', value='It is already paused', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}')
        await ctx.send(embed=embed)


@client.command()
async def resume(ctx):
    
    embed = Embed(timestamp = datetime.datetime.utcnow())
    embed.set_author(name='moosiqa bot', icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFNH7o1opnSCS_88e-bfYSYr_mnCas2zVUwA&usqp=CAU')
    

    voice = discord.utils.get(client.voice_clients)
    if voice.is_paused():
        embed.add_field(name='Resuming', value='Enjoy the goodness', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}')
        await ctx.send(embed=embed)
        voice.resume()
    else:
        embed.add_field(name='Already playing', value='It is already playing', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}')
        await ctx.send(embed=embed)


@client.command()
async def stop(ctx):

    embed = Embed(timestamp = datetime.datetime.utcnow())
    embed.set_author(name='moosiqa bot', icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFNH7o1opnSCS_88e-bfYSYr_mnCas2zVUwA&usqp=CAU')
    embed.add_field(name='Stopping', value='Stopped playing the current song', inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}')
    await ctx.send(embed=embed)
    
    voice = discord.utils.get(client.voice_clients)
    voice.stop()

client.run('YOU NEED TO USE YOUR OWN')
