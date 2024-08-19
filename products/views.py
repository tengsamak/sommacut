from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import CommentForm, Comment


def index(request):
    return HttpResponse('Hello')

def addcomment__testlink(request):
    return HttpResponse('/product/addcommnet')
from home.my_recaptcha import FormWithCaptcha
def addcomment(request,id):
    url=request.META.get('HTTP_REFERER') #CHECK the last url to return the same page
    #return HttpResponse(url)
    if request.method == 'POST':# check post
        form = CommentForm(request.POST)
        captcha=FormWithCaptcha(request.POST)
        if form.is_valid() and captcha.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.rate = form.cleaned_data['rate']     #add get for select
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)
        else:
            for key, error in list(captcha.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA ")
                    continue
                messages.error(request,error)
    captcha=FormWithCaptcha()
    return HttpResponseRedirect(url)

    #    form=CommentForm(request.POST)
    #    if form.is_valid():
    #        data=Comment() # create relation with Comment on model class
    #        data.subject=form.cleaned_data['subject']
    #        data.rate = form.cleaned_data['rate']
    #        data.comment=form.cleaned_data['comment']
    #        data.ip=request.META.get('REMOTE_ADDR')
    #       # print(data.subject,data.comment)
    #        data.product_id=id                      #check product id
    #        current_user=request.user                # check user login id
    #        data.user_id=current_user.id
    #        data.save()                                 # save data to table class model
    #        messages.success(request,'Your message has been sent, Thank you for your Comment Review.') # this message check and report to user
    #        return HttpResponseRedirect(url)

