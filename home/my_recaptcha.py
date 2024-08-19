from django import forms 

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

# class FormWithCaptcha(forms.Form):
#     #captcha = ReCaptchaField()
#     captcha = ReCaptchaField(
#     public_key='6LeBti8pAAAAAMYVX1AHQNvqIxNO7e5jMxKq_p0M',
#     private_key='6LeBti8pAAAAALaK4X84WTKhuWyyaiC2xljYSNoa',
# )
# class FormWithCaptcha(forms.Form):
#     #captcha = ReCaptchaField()
#     captcha = ReCaptchaField(
#         widget=ReCaptchaV2Checkbox(
#                 # attrs={
#                 # 'required_score': 0.85,
#                 # 'required':'True',
#                 #         }
#                 ),
#     # public_key='6LeBti8pAAAAAMYVX1AHQNvqIxNO7e5jMxKq_p0M',
#     # private_key='6LeBti8pAAAAALaK4X84WTKhuWyyaiC2xljYSNoa',
    
#     )
class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(),help_text="Please checked the requred Captcha",)