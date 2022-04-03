import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

url = 'https://www.nike.com/launch?s=upcoming'
r = requests.get(url=url)
src = r.content
shorba = BeautifulSoup(src, 'lxml')

month = [entry.text for entry in shorba.findAll('p',{'class':'headline-4'})]
day = [entry.text for entry in shorba.findAll('p',{'class':'headline-1'})]
shoe_line_1 = [entry.text for entry in shorba.findAll('h3',{'class':'headline-5'})]
shoe_line_2 = [entry.text for entry in shorba.findAll('h6',{'class':'headline-3'})]
links =  [f'https://www.nike.com{entry["href"]}' for entry in shorba.findAll('a',{'class':'card-link d-sm-b'})]

df = DataFrame()

for i in range(len('links')):
    
    temp = {}
    temp['name'] = f'{shoe_line_1[i]} {shoe_line_2[i]}'
    temp['month'] = month[i]
    temp['day'] = day[i]
    temp['date'] = f'{temp["month"]} {temp["day"]}'
    temp['link'] = links[i]

    url = links[i]
    r = requests.get(links[i])
    src = r.content
    shorba = BeautifulSoup(src, 'lxml')
   
    try:
        temp['price'] = [entry.text for entry in shorba.findAll('div',{'class':'headline-5 pb6-sm fs14-sm fs16-md'})][0]
    except: 
        pass

    df = df.append(temp,ignore_index=True)

df['price'] = df['price'].fillna('couldnt get price')
df.to_csv(f'./data/the sauce.csv')
print(df)
