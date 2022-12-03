from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from django.views.decorators.http import require_POST

from coupons.form import CouponApplyForm

from coupons.models import Coupons


def coupons(request):
    return HttpResponse('hello coupons')

@require_POST
def coupon_apply(request):
	now = timezone.now()
	form = CouponApplyForm(request.POST)
	if form.is_valid():
		code = form.cleaned_data['code']
		messages.info(request,code)
		try:
			coupon = Coupons.objects.get(code__iexact=code,
										valid_from__lte=now,
										valid_to__gte=now,
										active=True)
			request.session['coupon_id'] = coupon.id
			messages.info(request,"your coupon code success")
		except Coupons.DoesNotExist:
			messages.error(request,"your code error")
			request.session['coupon_id'] = None

		return redirect('shopcart')