from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from user.models import UserProfile
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm



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

def login_form(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user

            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            # *** Multi Langugae
           # request.session[translation.LANGUAGE_SESSION_KEY] = userprofile.language.code
            #request.session['currency'] = userprofile.currency.code
           #translation.activate(userprofile.language.code)

            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    category=Category.objects.all()
    context={'category':category,
             }
    return render(request,'login_form.html',context)


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


def logout_func(request):
    logout(request)
    messages.info(request,"You logged out.")
    return HttpResponseRedirect('/')

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
            return HttpResponseRedirect('/signup')
    form=SignUpForm()
    category=Category.objects.all()
    context={'category':category,
             'form':form,
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
                 }
        return render(request,'signup_form.html',context)





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
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
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


def indextest(request):
    return render(request,'indextest.html')