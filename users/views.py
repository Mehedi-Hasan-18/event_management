from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from users.forms import RegistrationForm,CustomSignInForm,CreateGroupForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.

def register(request):
    form = RegistrationForm()
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            
            messages.success(request, 'Please Varify Your Email')
            return redirect('signIn')
    return render(request, 'register.html', {'form':form})    

def signIn(request):
    form = CustomSignInForm()
    
    if request.method == 'POST':
        form = CustomSignInForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
        
    return render(request, 'signIn.html', {'form':form})
        
def signOut(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signIn')
    return render(request,'home.html')

@login_required
def active(request,user_id,token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('signIn')
        else:
            return HttpResponse("INVALID USERNAME OR TOKEN")
    except User.DoesNotExist:
        return HttpResponse("USER DOES NOT EXIST")
    
    
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success = f'Group Created SuccessFul'
        return redirect('dashboard')
    return render(request,'create_group.html', {'form':form})