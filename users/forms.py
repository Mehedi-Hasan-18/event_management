from events.forms import styleMixin
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User,Group,Permission
from django import forms
import re




class RegistrationForm(styleMixin,forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text='Must Contain both letters and numbers'
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already Exists")
        return email
    
    def clean_password(self):
        errors=[]
        
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            errors.append("⋅ At least 8 characters")
        if not re.search(r'[A-Z]',password):
            errors.append("⋅ Password Must include one Upper case leter")
        if not re.search(r'[a-z]',password):
            errors.append("⋅ Password Must include one lower case leter") 
        if not re.search(r'[0-9]',password):
            errors.append("⋅ Password Must include one number") 
        if not re.search(r'[@#$%^$+=]',password):
            errors.append("⋅ Password Must include atleast one speacial character") 
        
        if errors:
            raise forms.ValidationError(errors)
            
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Password do not Match")
        return cleaned_data
    
class CustomSignInForm(styleMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
            
            
class CreateGroupForm(styleMixin,forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Group' 
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']
    
        
        