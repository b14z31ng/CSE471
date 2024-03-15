from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_confirm_password(self):
        specialSym = ["$", "@", "#", "%", "*", "^", "!"]
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        if(len(password) <= 6):
            raise forms.ValidationError("Password must be greater than 6 character")
        
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must have at least one digit")
        
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must have at least one uppercase letter")
        
        if not any(char in specialSym for char in password):
            raise forms.ValidationError("Password must have at least one special character")
        

        return confirm_password


class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

# class EditUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']