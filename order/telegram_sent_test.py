

TOKEN="7043199444:AAGRP4Uo25wOHY6_7Y-rbtWCV-iTxGMDPUg"
CHAT_ID="-4159721907"
#import requests
#url= f"https://api.telegram.org/bot{TOKEN}/sendMessage"
# URL TO GET CHAT_ID:
#url= f"https://api.telegram.org/bot{TOKEN}/getUpdates"

#ULR TO ACTUALLY SEND TELEGRAM MESSAGE:
#url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
#print(requests.get(url).json())

import requests
# import datetime # change datetime
from django.utils.timezone import datetime
def sent_to_telegram(otpcode,phonenum):

        # today = format(datetime.datetime.now()) # change datetime
        today = format(datetime.now())
        print("todaydate:",today)
        message =today+" :OTP Verify: "+str(otpcode)+" PhoneNumber: "+str(phonenum)
        #for sent file to group
        filesent={'photo':open('D:\\file\somma.png','rb')}
        sentfile={'document':open('D:\\file\somma.pdf','rb')}
        urlmsg = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&caption="Somma MSG"'
        urlphoto = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={CHAT_ID}&text={message}&caption=somma Photo"
        urlfile= f"https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={CHAT_ID}&text={message}&caption=SoMMa Invoice"
        #resp=requests.post('https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={CHAT_ID}',files=filesent)
        #print(resp.text)
        re= requests.post(urlmsg)
        #re=requests.post(urlphoto,files=filesent)
        #re=requests.post(urlfile,files=sentfile)
        print(re.json())
