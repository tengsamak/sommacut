from django import forms


class CouponApplyForm(forms.Form):
	# TODO: Define form fields here
	code = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Please input code'}))