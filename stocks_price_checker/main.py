import discord
from scraper import scripity_scrape

# create a new client instance, connection to discord
client = discord.Client()
 
@client.event
async def on_ready():
    print('beep boop....')

@client.event
async def on_message(message):

    if message.author == client:
        return

    if message.content.startswith('$') and message.content.lower() != '$help' and len(message.content) < 6:
        ticker_name = scripity_scrape(message.content[1:])[0][0]
        ticker_price = scripity_scrape(message.content[1:])[1][0]
        await message.channel.send(f'{ticker_name} is currently ${ticker_price}')

    if message.content.lower() == '$help':
        await message.channel.send('To get the current price of a stock, type $ followed by the ticker \nExample $JNUG')

client.run('you need your own')
