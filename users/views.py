from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from users.forms import RegistrationForm,CustomSignInForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.views.generic import CreateView,View,TemplateView
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordResetConfirmView,PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordContextMixin



def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_perticipant(user):
    return user.groups.filter(name='Participant').exists()

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('signIn')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()
    
        messages.success(self.request, 'Please verify your email')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    form_class = CustomSignInForm
    template_name = 'signIn.html'
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
 
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('signIn')
        

class AccountActivationView(View):
    def get(self,request,user_id,token):
        try:
            user = User.objects.get(id=user_id)
            if not default_token_generator.check_token(user,token):
                messages.error(request,"Invalid Activation Link")
                return redirect('signIn')
            user.is_active = True
            user.save()

            messages.success(request, "Account Activation Successfully Done!")
            return redirect('signIn')
        except User.DoesNotExist:
            messages.error(request, "User Does Not Exist")
            return redirect("register")

@method_decorator(permission_required(is_admin,login_url='signIn') ,name='dispatch')
class CreateGroupView(CreateView):
    form_class = CreateGroupForm
    template_name = 'create_group.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Group Created Successfully!")
        return response

class ProfileView(TemplateView):
    template_name = 'accounts\profile.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = self.request.user
        
        context['username'] = users.username
        context['email'] = users.email
        context['name'] = users.get_full_name()
        context['member_since'] = users.date_joined
        context['last_login'] = users.last_login
        
        return context

class ChangePassword(PasswordChangeView):
    template_name='accounts/password_change.html'
    form_class = CustomPasswordChangeForm
    
class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_change_done.html"
    title = ("Password change successful")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registers/reset_password.html'
    success_url = reverse_lazy('signIn')
    html_email_template_name = 'registers/reset_email.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request,'A password Reset Email Send')
        return super().form_valid(form)

class CustomPasswordReseConfirmtView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registers/reset_password.html'
    success_url = reverse_lazy('signIn')
    
    
    def form_valid(self, form):
        messages.success(self.request,'Password Reset SuccessFully')
        return super().form_valid(form)