# Purpose: send an email/text reminder for AMD's GPU restock.
# occurs everything thursday 1:35 PM UTC 

import yagmail
import calendar
from datetime import date, datetime

amd = 'https://www.amd.com/en/direct-buy/us'
to = ['']

# utc time
drop_oclock = '13:35'
drop_day = 'Thursday'

while True:
    if calendar.day_name[date.today().weekday()] == drop_day:
        if datetime.utcnow().strftime('%H:%M') == drop_oclock:

            auth = {
                'user':''
                , 'app_pass':''
            }
            
            with yagmail.SMTP(auth['user'],auth['app_pass']) as yag:
                yag.send(bcc=to,subject='AMD Queue Starting Soon', contents=f'Join now to make it in time for the queue.\n{amd}')
