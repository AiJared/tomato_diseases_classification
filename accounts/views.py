from django.shortcuts import render

import datetime
from accounts.decorators import administrator_required, client_required
from accounts.tokens import account_activation_token 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string 
from accounts.models import Administrator, Client, User, Services, Itworks
from accounts.sendMails import  send_activation_email
from accounts.forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView

decorators = [never_cache, login_required, administrator_required]

def homepage(request):
    itworks = Itworks.objects.all()
    services = Services.objects.all()

    context = {
        'itworks':itworks,
        'services':services,
    }

    return render(request, 'index.html',context)

def clientRegistration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get('password')
        password2 = request.POST.get('confirm-password')

        if password != password2:
            messages.error(request,"Password didn't match")
            return render(request,'accounts/sign_up.html')
        user = User(email=email, username=username, first_name=first_name, last_name=last_name)
        user.set_password(password2)
        user.is_active = False
        user.save()
        send_activation_email(user,request)
        
        client = Client(user=user)
        client.save()
        messages.success(request,"Account created succesfully")
        return render(request,'accounts/sign_alert.html')
    return render(request,'accounts/sign_up.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user= User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'email does not exist!') 
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Logged in succesfully')
                return render(request, 'classifier/classifier_model.html', {})
            else:
                messages.error(request, 'Please activate your account')
                return redirect('/login/') 
        else:
            messages.error(request, 'Incorrect password')
            return redirect('/accounts/login/')
    return render(request,'accounts/login.html')


#logout the logged in user   
def log_out(request):
    logout(request)
    return redirect('/')

def RequestPasswordReset(request):
    context = {
        # Add context data as needed
    }
    return render(request, "accounts/RequestPasswordReset.html", context)



def activate(request, uidb64, token):  
    User = get_user_model() 
    
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        login(request,user)  
        messages.success(request,"Account was Successfully Verified.")
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')


def edit_profile(request):
    r_user = User.objects.get(id=request.user.id)
    user = Client.objects.get(user=r_user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user, user=r_user)
        if form.is_valid():
            # phone = form.cleaned_data['phone']
            full_name = form.cleaned_data['full_name']
            town = form.cleaned_data['town']
            county = form.cleaned_data['county']
            username = form.cleaned_data['username']
            password2 = form.cleaned_data['password2']
            # image = request.FILES['image']
            if len(request.FILES) != 0:
                if len(user.profile_picture) > 0:
                    user.profile_picture = request.FILES['image']
            form.save()
            # r_user.phone = phone
            r_user.full_name = full_name
            r_user.username = username
            r_user.town = town
            r_user.county = county
            r_user.save()
            if len(password2) > 0:
                r_user.set_password(password2)
            messages.success(request, 'Updated succesfully')
            return redirect('/dashboard/')
    else:
        form = ProfileForm(instance=user, user=r_user)

    return render(request, 'accounts/profile.html', {'form': form,'user':user})