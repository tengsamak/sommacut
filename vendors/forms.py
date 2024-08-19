from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput

from vendors.models import Vendor


class VendorUserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'first_name'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'last_name' }),
        }

#CITY = [
#    ('Istanbul', 'Istanbul'),
#    ('Ankara', 'Ankara'),
#    ('Izmir', 'Izmir'),
#]
class VendorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('companyname', 'contactname', 'address1', 'phone1')
        widgets = {
            'companyname': TextInput(attrs={'class': 'input', 'placeholder': 'companyname'}),
            'contactname': TextInput(attrs={'class': 'input', 'placeholder': 'contactname'}),
            'address1': TextInput(attrs={'class': 'input', 'placeholder': 'address1'}),
            'phone1': TextInput(attrs={'class': 'input', 'placeholder': 'phone1'}),
          #  'status': TextInput(attrs={'class': 'input', 'placeholder': 'status'}),
           # 'create_at': Text(attrs={'class': 'input', 'placeholder': 'create_at'}),
            #'update_at': TextInput(attrs={'class': 'input', 'placeholder': 'update_at'}),
        }