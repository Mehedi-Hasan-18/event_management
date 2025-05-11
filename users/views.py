from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from users.forms import RegistrationForm,CustomSignInForm,CreateGroupForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required

# Create your views here.

def register(request):
    form = RegistrationForm()
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save() 
            
            messages.success(request, 'Please verify your email')
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

def active(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated. Please log in.')
            return redirect('signIn')
        else:
            messages.error(request, 'Invalid activation link')
            return redirect('signIn')
    except User.DoesNotExist:
        messages.error(request, 'User does not exist')
        return redirect('signIn')
    
@login_required
# @permission_required('auth.add_group', login_url='signIn')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success = f'Group Created SuccessFul'
        return redirect('dashboard')
    return render(request,'create_group.html', {'form':form})