import pyotp
#from datetime import datetime,timedelta # change datetime
from django.utils.timezone import datetime,timedelta

from countdowntime import countdown
#def sent_otp(request,number):
totp=pyotp.TOTP(pyotp.random_base32(),interval=60) #,interval=60
otp=totp.now()
# hotp = pyotp.HOTP(pyotp.random_base32())
# hotp.at(1)
#request.session['otp_secret_key']=totp.secret
valid_date=datetime.now() + timedelta(minutes=5)
#request.session['otp_valid_date'] = str(valid_date)
print(f"Your OTP is {otp}")
print(f"Your OTP secrete key is {totp.secret}")
print(f"Your Valid date is {valid_date}")
print(f"Your date now is {datetime.now()}")
print(f"Your interval is {totp.interval - datetime.now().timestamp() % totp.interval}")
print(f"Your timestamp is {datetime.now().timestamp()}")
print(f"Your totpinverval is {totp.interval}")

#print(f"Your the phone number request {number}")
#    return otp
# input time in seconds 
#t = input("Enter the time in seconds: ") 
#print(f"time sleep {time.sleep(30)}")
x=totp.interval - datetime.now().timestamp() % totp.interval
t = x+10 
print(f"timecount{t}")
# function call 
countdown(int(t))

#def verify_otp():
#code=input("you code=")
#key=input("your key=")

totp=pyotp.TOTP(totp.secret,interval=60)
if totp.verify(otp,valid_window=7): #valid_window=7 for time available in windows
        print("valid code and key")
else:
        print("invalid code")



  