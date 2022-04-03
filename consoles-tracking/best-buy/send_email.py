import yagmail
import secrets 

def send(message,subject,to):
    auth = {
        'user':secrets.app_user,
        'app_pass':secrets.app_pass
    }
    
    with yagmail.SMTP(auth['user'], auth['app_pass']) as yag:
        yag.send(bcc=to, subject=subject, contents=message)
