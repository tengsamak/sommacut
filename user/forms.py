from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput
from django.contrib.auth import get_user_model
from user.models import UserProfile
from home.my_recaptcha import FormWithCaptcha
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class SignUpForm(UserCreationForm):
    # username=forms.CharField(max_length=30,label='User Name:')
    # email=forms.EmailField(max_length=200,label='Email:')
    # first_name=forms.CharField(max_length=100,help_text='First Name',label='First Name:')
    # last_name=forms.CharField(max_length=100,help_text='Last Name',label='Last Name:')
    #captcha = FormWithCaptcha() # ->add captcha
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(),help_text="Please checked the requred Captcha",)
    class Meta:
        model=User
        fields=['username',
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                
        ]
        # test signup form with widgets
        widgets = {
            'username': forms.TextInput(attrs={
                'class':'form-control ftsize',
                'type':"text",
                'placeholder':"Enter User Name",
                'name':"username",
            }),
            'email': forms.EmailInput(attrs={
                'class':'form-control ftsize',
                'type':"email",
                'placeholder':"Enter Email",
                'name':"email",
            }),
           
            'first_name': forms.TextInput(attrs={
                'class':'form-control ftsize',
                'type':'text',
                'placeholder':'Fist Name',
                'name':'first_name',
            }),
            'last_name': forms.TextInput(attrs={
                'class':'form-control ftsize',
                'type':"text",
                'placeholder':"last name",
                'name':"last_name",
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control ftsize',
                'type': "password",
                'placeholder': "Enter Password",
                'name': "password1",
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control ftsize',
                'type': "Repeat Password",
                'placeholder': "Repeat Password",
                'name': "password2",
            }),
        }
        
#from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.formfields import PhoneNumberField
class SignUpViaPhone(SignUpForm):
    phonenumber=PhoneNumberField(region="KH")
    # class Meta:
    #     medel =  get_user_model
    #     fields=['username',
                
    #             'first_name',
    #             'last_name',
    #             'password1',
    #             'password2',
                
    #     ]
        # widgets = {
        #     'username'  : TextInput(attrs={'class': 'form-control','placeholder':'username'}),
        # }
    
# Createformlogintest
# class Login___Form(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(Login___Form, self).__init__(*args, **kwargs)
#         # test signup form with widgets
#
#         username: forms.CharField(widget=forms.TextInput(attrs={
#                 'class': "",
#                 'type': "text",
#                 'placeholder': "SommA",
#                 'name': "username",
#             }))
#         password: forms.CharField(widget=forms.PasswordInput(attrs={
#                 'class': "",
#                 'type': "password",
#                 'placeholder': "Teng",
#                 'name': "password",
#             }))



class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'form-control','placeholder':'username'}),
            'email'     : EmailInput(attrs={'class': 'form-control','placeholder':'email'}),
            'first_name': TextInput(attrs={'class': 'form-control','placeholder':'first_name'}),
            'last_name' : TextInput(attrs={'class': 'form-control','placeholder':'last_name' }),
        }

CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city','country','image')
        widgets = {
            'phone'     : TextInput(attrs={'class': 'form-control','placeholder':'phone'}),
            'address'   : TextInput(attrs={'class': 'form-control','placeholder':'address'}),
            'city'      : Select(attrs={'class': 'form-control','placeholder':'city'},choices=CITY),
            'country'   : TextInput(attrs={'class': 'form-control','placeholder':'country' }),
            'image'     : FileInput(attrs={'class': 'form-control', 'placeholder': 'image','type':'file' }),
        }
        
#create form ke thua the existing form 
#from django.contrib.auth import get_user_model
class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        medel =  get_user_model()
        fields =  ('old_password','new_password1','new_password2')
        widgets = {
            'old_password'     : TextInput(attrs={'class': 'form-control','placeholder':'please input old password'}),
            'new_password1'   : TextInput(attrs={'class': 'form-control','placeholder':'please input new password'}),
            'new_password2'      : TextInput(attrs={'class': 'form-control','placeholder':'please input new password'}),
        }
        
class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        
#for forgetpassword via submite email
class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
        widget = {
            'new_password1' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'please input new password','type':"password"}),
            'new_password2' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'please input new password','type':"password"}),
        }
        
#for newletter form

from ckeditor.fields import RichTextFormField
class NewsletterForm(forms.Form):
    subject = forms.CharField()
    receivers = forms.CharField()
    #message = forms.CharField(widget=TinyMCE(), label="Email content") 
    messagedetail = RichTextFormField()