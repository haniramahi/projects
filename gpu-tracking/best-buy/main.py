# takes less than 1 minute to run script. only checks for items once, does not loop
# need to schedule this to run on the server every minute.

import secrets
import requests
import time
from send_email import send

to = secrets.to

# add desired gpus to track
# key = item name, value = sku from best buy's website
gpus = {
    'rtx3070': '6465789',
    'rtx3080': '6429440',
    'rtx3080ti': '6462956'
}

# if only specific stores desired, enter store name and store id into dictionary
stores = {
    'bolingbrook': '813',
    'downers grove (butterfield)': '301',
    'downers grove (lemont)': '316'
}

# to pull all stores around a zipcode, uncomment the code below and update the zipcode variable
# zip_code = '55423'
# url = f'https://api.bestbuy.com/v1/stores(postalCode={zip_code})?format=json&show=storeId,storeType,name,city,region&apiKey={secrets.apiKey}'
# r = requests.get(url=url)
# res = r.json()

# store_id = [i['storeId'] for i in res['stores']]
# store_name = [i['name'] for i in res['stores']]
# stores = {store_name[i]: store_id[i] for i in range(len(store_name))}

for store, storeId in stores.items():

    params = {
        'format':'json',
        'apiKey':secrets.apiKey,
        'storeId':storeId
    }

    for gpu, sku in gpus.items():
        print(f'checking for {gpu} in {store}')

        # send request
        r = requests.get(url=f'https://api.bestbuy.com/v1/products/{sku}/stores.json', params=params)
        print(f'Request sent: {r.url}')
        resp = r.json()

        try:
            if resp['ispuEligible'] is True:
                print(f'found {gpu} at {store}')
                print(f'https://api.bestbuy.com/click/-/{sku}/cart\n')
                send(to=to, subject=f'Found {gpu} at {store}', message=f'ATC: https://api.bestbuy.com/click/-/{sku}/cart')
            elif resp['ispuEligible'] is False:
                print('found nothing. time to sleep, goodnight\n')
        except KeyError:
            time.sleep(5)
            print(KeyError)

        time.sleep(5)
