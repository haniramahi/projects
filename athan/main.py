import discord
import requests
from datetime import datetime
from pandas import json_normalize

# default city, country
city = 'Bolingbrook'
country = 'United States of America'

# create a new client instance, connection to discord
client = discord.Client()

# function to get prayer times from API
def get_prayer_times(city,country):

    # parameters needed for API
    params = {

        'city': city,
        'country': country,
        'method': '2',
        'month': datetime.today().month,
        'year': datetime.today().year

    }

    r = requests.get('http://api.aladhan.com/v1/calendarByCity', params = params)
    resp = r.json()
    prayer_times = json_normalize(resp['data'])
    return prayer_times
 
@client.event
async def on_ready():
    print('beep boop....')

@client.event
async def on_message(message):
   
    df = get_prayer_times(city,country)
    today_df = df.loc[df['date.gregorian.day'] == f'0{datetime.today().day}' if datetime.today().day < 10 else datetime.today().day]
    
    if message.author == client:
        return

    for i in ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
        if message.content.title() == f'!{i}':
            # get time of prayer from df
            time = today_df['timings.'+i].item()

            # convert from 24hr to 12hr, then display
            t = datetime.strptime(time[:5], '%H:%M')
            await message.channel.send(f'{t.strftime("%I:%M %p")}')

    if message.content.lower() == '!help':
        await message.channel.send('To get prayer times, type ! followed by the prayer\n Example - !asr')
        # await message.channel.send('To see current settings, type ! followed by settings\n Example - !settings')
        # await message.channel.send('To configure, type ! followed by configure\n Example - !configure')
        
client.run('')
