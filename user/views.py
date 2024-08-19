from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from user.models import UserProfile
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm




# Create your views here.
from products.models import Category,Comment

from order.models import Order, OrderProduct

from home.models import FAQ

from vendors.models import Vendor

from products.models import Product


@login_required(login_url='/login') # Check login
def index(request): # test link
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
   #  usersocial = authenticate(current_user)
   #  if usersocial is not None:
   #      data = UserProfile()
   #      data.user_id = current_user.id
   # # data.image = "images/users/user.png"
   #      data.save()
   #  else:
    profile = UserProfile.objects.get(user_id=current_user.id)
    if profile.usertype == "VENDOR":

       # vendorprofile=Vendor.objects.get_or_create(user_id=current_user.id)
        vendorprofile = Vendor.objects.filter(user_id=current_user.id).get_or_create(user_id=current_user.id)
        #print(vendorprofile)
        vendorprofile1= Vendor.objects.get(user_id=current_user.id)
        context = {'category': category,
                   'profile': profile,
                    'vendorprofile': vendorprofile,
                   'vendorprofile1': vendorprofile1,

                   }
        return render(request, 'user_profile.html', context)


    #usersocial=authenticate(request,user_id=current_user.id)
    # if usersocial is not None:
    #     data=UserProfile()
    #     data.user_id = current_user.id
    #    # data.image = "images/users/user.png"
    #     data.save()
    #     context={'category': category,
    #              'usersocial':usersocial,
    #     }
    #     return render(request, 'user_profile.html', context)


    #
    #
    context = {'category': category,
               'profile':profile,
             #  'vendorprofile':vendorprofile,
           }
    return render(request, 'user_profile.html', context)

from home.my_recaptcha import FormWithCaptcha
def login_form(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            current_user = request.user

            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            # *** Multi Langugae
           # request.session[translation.LANGUAGE_SESSION_KEY] = userprofile.language.code
            #request.session['currency'] = userprofile.currency.code
           #translation.activate(userprofile.language.code)

            # Redirect to a success page.
            messages.success(request,"Success Login!")
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.
    #messages.warning(request, "Login Error !! Username or Password is incorrect")    
    #category=Category.objects.all()
    #context={'category':category,
    #         }
    return render(request,'login_form.html',{'captcha':FormWithCaptcha,})

#test login after email verify click update to userprofile
def login__1form(request): #backup
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password'] 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            current_user = request.user
            if UserProfile.objects.filter(user_id=current_user.id).exists():
                userprofile = UserProfile.objects.get(user_id=current_user.id)
                request.session['userimage'] = userprofile.image.url
            else:
                # after autologin Create data in profile table for user userprofile table
                #current_user=request.user
                data=UserProfile()
                data.user_id=current_user.id
                data.image="images/users/user.png"
                data.save()
                messages.success(request,'Your account PROFILEUPDATE has been created!')
                
            # Redirect to a success page.
            messages.success(request,"Success Login!")
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
        #endold
    return render(request,'login_form.html',{'captcha':FormWithCaptcha,})

##test login after email verify click update to userprofile
# for test recaptcha
def login__form(request):
    if request.method=='POST':
        # username = request.POST['username']
        # password = request.POST['password']
        captcha=FormWithCaptcha(request.POST)
        #user = authenticate(request, username=username, password=password)
        if captcha.is_valid():  
            username = request.POST['username']
            password = request.POST['password']
            #old
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                current_user = request.user
                if UserProfile.objects.filter(user_id=current_user.id).exists():
                    userprofile = UserProfile.objects.get(user_id=current_user.id)
                    request.session['userimage'] = userprofile.image.url
                else:
                    # after autologin Create data in profile table for user userprofile table
                    #current_user=request.user
                    data=UserProfile()
                    data.user_id=current_user.id
                    data.image="images/users/user.png"
                    data.save()
                    messages.success(request,'Your account PROFILEUPDATE has been created!')
                    
                # Redirect to a success page.
                messages.success(request,"Success Login!")
                return HttpResponseRedirect('/')
        else: # Form or chaptcha not valid
            #captcha=FormWithCaptcha()
            for key, error in list(captcha.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA ")
                    continue
                messages.error(request,error)
            #return HttpResponseRedirect('/login')
        #endold
        # else: # captcha form is not valid
        #     captcha=FormWithCaptcha()
        #     messages.warning(request, "Not Check Captcha")
    #else: # form login not post
    captcha=FormWithCaptcha()
    #messages.warning(request, "Please input the requirement fields")        
        
    return render(request,'login_form.html',{'captcha':captcha})

# testloginform by create loginform
def login___form(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            current_user = request.user
            #********
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            #********
            messages.info(request,"you're loggin...")
            return redirect('/')
        else:
            messages.warning(request,"Invalid User")
            return redirect('login_form')
    else:
        #return redirect('login_form')

        # form =AuthenticationForm(request=request,data=request.POST)
        # if form.is_valid():
        #     username=form.cleaned_data['username']
        #     password=form.cleaned_data['password']
        #     user=authenticate(username=username,password=password)
        #     if user is not None:
        #         auth.login(request, user)
        #         # Print alert message
        #         messages.error(request, 'You logged in samak.')
        #         #login(request,user)
        #         current_user = request.user
        #         userprofile = UserProfile.objects.get(user_id=current_user.id)
        #         request.session['userimage'] = userprofile.image.url
        #         return HttpResponseRedirect('/')
        #     else:
        #         messages.warning(request, "Login Error !! Username or Password is incorrect")
        #         return HttpResponseRedirect('/login')
        form=AuthenticationForm()
        category = Category.objects.all()
        context = {'category': category,
                   'form':form,
                   }
        return render(request, 'login_form.html', context)

@login_required(login_url='/login') # Check login
def logout_func(request):
    logout(request)
    messages.info(request,"You logged out.")
    return HttpResponseRedirect('/')

def forgetpassword(request):
    # context = {'category': category,
    #                'form':form,
    #                }
    return render(request, 'login_forgetpassword.html',{'captcha':FormWithCaptcha,})

#password reset or forget password by email
#@user_not_authenticated
from django.db.models.query_utils import Q
def password_reset_request(request):
    if request.method == 'POST':
        user_email = request.POST['email']
        #print(user_email)
        #form = PasswordResetForm(request.POST)
        # if form.is_valid():
        #     user_email = form.cleaned_data['email']
        associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
        if associated_user:
            subject = "Password Reset request"
            message = render_to_string("template_reset_password.html", {
                'user': associated_user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                'token': account_activation_token.make_token(associated_user),
                "protocol": 'https' if request.is_secure() else 'http'
                })
            email = EmailMessage(subject, message, to=[associated_user.email])
            if email.send():
                messages.success(request, f'Dear <b>Value Customer</b>, please go to you email <b>{user_email}</b> inbox and click on \
                received reset_password link to confirm and complete the reset. <b>Note:</b> Check your spam folder.')
                messages.success(request,
                    """
                    <h2>Password reset sent</h2><hr>
                    <p>
                        We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                        You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                        you registered with, and check your spam folder.
                    </p>
                    """
                    )
            else:
                messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")
            
            return redirect('/forgetpassword')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA ")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="login_forgetpassword.html",
        #template_name="password_reset.html", 
        
        context={"form": form,'captcha':FormWithCaptcha,}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            # newpasw1=request.POST['newpasw1']
            # newpasw2=request.POST['newpasw2']
            form = SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('/login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("/")


def signup_form(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Your Account Created Successful!! Happy Shopping")
            form.save() # Form Signup form completed
            username=form.cleaned_data.get('username') #login after signup
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            # after autologin Create data in profile table for user userprofile table
            current_user=request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request,'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup',{'captcha':FormWithCaptcha,})
    form=SignUpForm()
    category=Category.objects.all()
    context={'category':category,
             'form':form,
             'captcha':FormWithCaptcha,
             }
    return render(request,'signup_form.html',context)


# testSignup check validate and alert menssage
def signup___form(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        # password1=request.POST['password1']
        # password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            #print('Sorry!Username is taken.')
            messages.error(request,'Sorry!,User Name is taken.')
            return redirect('signup_form')
        elif User.objects.filter(email=email).exists():
            #print("Sorry!,Email is taken.")
            messages.error(request,'Sorry!,Your Email is registered already..')
            return redirect('signup_form')
        else:
            form = SignUpForm(request.POST)
            if form.is_valid():
                messages.success(request, "Your Account Created Successful!! Happy Shopping")
                form.save()  # Form Signup form completed
                username = form.cleaned_data.get('username')  # login after signup
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                # after autologin Create data in profile table for user userprofile table
                current_user = request.user
                data = UserProfile()# for userprofile table
                data.user_id = current_user.id
                data.image = "images/users/user.png"
                data.save()
                messages.success(request, 'Your account has been created!')
                return HttpResponseRedirect('/')
            else:
                messages.warning(request, form.errors)
                return HttpResponseRedirect('/signup')

    else:
        form=SignUpForm()
        category=Category.objects.all()
        context={'category':category,
                 'form':form,
                 'captcha':FormWithCaptcha,
                 }
        return render(request,'signup_form.html',context)

# signup with email verify
def register1(request): #backup
    if request.method == "POST":
        #--------
        username=request.POST['username']
        email=request.POST['email']
        # password1=request.POST['password1']
        # password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            #print('Sorry!Username is taken.')
            messages.error(request,'Sorry!,User Name is taken.')
            return redirect('signup_form')
        elif User.objects.filter(email=email).exists():
            #print("Sorry!,Email is taken.")
            messages.error(request,'Sorry!,Your Email is registered already..')
            return redirect('signup_form')
        else:
        #--------
        
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active=False
                user.save()
                activateEmail(request, user, form.cleaned_data.get('email'))
                print("please check email for activated!")
                return redirect('/login')

            else:
                for error in list(form.errors.values()):
                    print("you get error signup")
                    messages.error(request, error)

    else:
        form = SignUpForm()
    category=Category.objects.all()
    context={'category':category,
            'form':form,
            'captcha':FormWithCaptcha,
            }
    return render(request,'signup_form.html',context)

#signup with recaptcha
def register(request):
    if request.method == "POST":
        #--------
        username=request.POST['username']
        email=request.POST['email']
        # password1=request.POST['password1']
        # password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            #print('Sorry!Username is taken.')
            messages.error(request,'Sorry!,User Name is taken.')
            return redirect('signup_form')
        elif User.objects.filter(email=email).exists():
            #print("Sorry!,Email is taken.")
            messages.error(request,f'Sorry!,Your Email is registered already..')
            return redirect('signup_form')
        else:
        #--------
            form = SignUpForm(request.POST)
            #captcha = FormWithCaptcha(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active=False
                user.save()
                # messages.info(request,f'success')
                activateEmail(request, user, form.cleaned_data.get('email'))
                print("please check email for activated!")
                return redirect('/login')
                #return redirect('/signup')

            else:
                for key, error in list(form.errors.items()):
                    if key == 'captcha' and error[0] == 'This field is required.':
                        messages.error(request, "You must pass the reCAPTCHA ")
                        continue
                    else:
                        messages.error(request, error)

    else:
        form = SignUpForm()
        #captcha = FormWithCaptcha()
    #phonefrm=SignUpViaPhone()
    category=Category.objects.all()
    context={'category':category,
            'form':form,
            #'captcha':captcha,
            #'phonefrm':phonefrm,
            }
    return render(request,'signup_form.html',context)



#activate Email function
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

#activate function via email
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        print("your acc activated!!!!! please login")
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        
        # after autologin Create data in profile table for user userprofile table
        # current_user=request.user
        # data=UserProfile()
        # data.user_id=current_user
        # data.image="images/users/user.png"
        # data.save()
        #end update profile
        return redirect('/login')
    else:
        print("Activation link is invalid!")
        messages.error(request, "Activation link is invalid!")

    return redirect('/')


@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login') # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            logout(request) # after success change password process logout and sigin with new password change
            return HttpResponseRedirect('/login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            # messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            # return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,'category': category })

@login_required(login_url='/login') # Check login
def user_orders(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    orders = Order.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'orders': orders,}
    return render(request, 'user_orders.html', context)

@login_required(login_url='/login') # Check login
def user_orderdetail(request,id):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    orders = Order.objects.get(user_id=current_user.id,id=id)
    orderitems=OrderProduct.objects.filter(order_id=id)
    context = {'category': category,
               'orders': orders,
               'orderitems': orderitems,}
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login') # Check login
def user_order_product(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    # order = Order.objects.get(user_id=current_user.id, id=id)
    order_product = OrderProduct.objects.filter(user_id=current_user.id)
    context = {'category': category,
               # 'orders': order,
               'order_product': order_product, }
    return render(request, 'user_order_product.html', context)

@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    orders = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)

    # test get vendor company name from product ID
    #vendorcompanyname=Product.objects.filter(orderitems__product_id=id)
   # vv=Vendor.objects.filter(vendorcompanyname__vendor_id=id)
   # print(vv)
    context = {'category': category,
               'orders': orders,
               'orderitems': orderitems,
              # 'vv': vv,

               }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login') # Check login
def user_comments(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    comments=Comment.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'comments': comments,
               }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login') # Check login
def user_deletecomment(request,id):
    current_user=request.user
    Comment.objects.filter(id=id,user_id=current_user.id).delete()
    messages.success(request,'Comment Delete..!')
    return HttpResponseRedirect('/user/comments')

def faq(request):
    category=Category.objects.all()
    faq=FAQ.objects.filter(status="True").order_by("ordernumber")
    context={
        'category':category,
        'faq':faq,
    }
    return render(request,'faq.html',context)

# copy from https://stackoverflow.com/questions/14523224/how-to-populate-user-profile-with-django-allauth-provider-information
@login_required(login_url='/login') # Check login
def populate_profile(sociallogin, user, **kwargs):

    if sociallogin.account.provider == 'facebook':
        user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"
        email = user_data['email']
        first_name = user_data['first_name']

    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        picture_url = user_data['picture-urls']['picture-url']
        email = user_data['email-address']
        first_name = user_data['first-name']

    if sociallogin.account.provider == 'twitter':
        user_data = user.socialaccount_set.filter(provider='twitter')[0].extra_data
        picture_url = user_data['profile_image_url']
        picture_url = picture_url.rsplit("_", 1)[0] + "." + picture_url.rsplit(".", 1)[1]
        email = user_data['email']
        first_name = user_data['name'].split()[0]

    user.profile.image = picture_url
    user.profile.email_address = email
    user.profile.first_name = first_name
    user.profile.save()

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import SubscribedUsers
# subscribe function
def subscribe(request):
    if request.method == 'POST':
        #name = request.POST.get('name', None)
        email = request.POST.get('email', None)

        #if not name or not email:
        if not email:    
            messages.error(request, "You must type legit name and email to subscribe to a Newsletter")
            print("You must type legit name and email to subscribe to a Newsletter")
            return redirect("/")

        if get_user_model().objects.filter(email=email).first():
            messages.error(request, f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            print("You must login to subscribe or unsubscribe.")
            return redirect(request.META.get("HTTP_REFERER", "/")) 

        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f"{email} email address is already subscriber.")
            print("email address is already subscriber..")
            return redirect(request.META.get("HTTP_REFERER", "/"))  

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        subscribe_model_instance = SubscribedUsers()
        #subscribe_model_instance.name = name
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        print("email was successfully subscribed to our newsletter!")
        return redirect(request.META.get("HTTP_REFERER", "/"))      

#for Newletter superuser sent email the the user and subscriber email list
from .forms import NewsletterForm
from .decorators import user_is_superuser
@user_is_superuser
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers').split(',')
            email_message = form.cleaned_data.get('message')

            mail = EmailMessage(subject, email_message, f"SoMMa store <{request.user.email}>", bcc=receivers)
            mail.content_subtype = 'html'

            if mail.send():
                messages.success(request, "Email sent succesfully")
            else:
                messages.error(request, "There was an error sending email")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

        return redirect('/')

    form = NewsletterForm()
    form.fields['receivers'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
    return render(request=request, template_name='user_profile.html', context={'form': form})
from .forms import SignUpViaPhone
def signupviaphone(request):
    if request.method == 'POST':
        form = SignUpViaPhone(request.POST)
        if form.is_valid():
            pass
    else:
        pass
    form = SignUpViaPhone()
    context={
            'phonefrm':form,
        }
    print(context)
    return render(request,'signup_form.html',context)
    
def indextest(request):
    #return render(request,'indextest.html')
    
    form = SetPasswordForm(request.POST)
    print(form)
    return render(request, 'recover-password.html', {'form': form})
    
    #return render(request,'password_reset_confirm.html')

