import pyotp
from datetime import datetime,timedelta
def sent_otp(request,number):
    totp=pyotp.TOTP(pyotp.random_base32(),interval=180)
    otp=totp.now()
    request.session['otp_secret_key']=totp.secret
    valid_date=datetime.now() + timedelta(minutes=3)
    request.session['otp_valid_date'] = str(valid_date)
    print(f"Your OTP is {otp}")
    print(f"Your OTP secrete key is {totp.secret}")
    print(f"Your the phone number request {number}")
    return otp

# def verify_otp():
#     code=input("you code:")
#     key=input("your key:")
#     totp=pyotp.TOTP(key,interval=240)
#     if totp.verify(code):
#         print("valid code and key")
#     else:
#         print("invalid code")
    


    