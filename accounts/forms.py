from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
import re
from django.forms import ValidationError

class CreateUser(forms.ModelForm):
    password_1 = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email','username']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        if not re.search(r'\.(com|net|org|edu)$', email, re.IGNORECASE):
            raise forms.ValidationError("Email must end with .com, .net, .org, or .edu")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username already exists')
        if len(username) < 8:
            raise forms.ValidationError('username cant be less than 8 characters')
        if username[0].isdigit():
            raise forms.ValidationError('username cant start with a number')
        return username
    
    def clean_password_2(self):
        data = self.cleaned_data
        if not data['password_1'] or not data['password_2']:
            raise forms.ValidationError('password field are empty')
        if len(data['password_2']) < 8:
            raise forms.ValidationError('password must be at least 8 charecters')        
        if data['password_2'] != data['password_1']:
            raise forms.ValidationError('passwords are not the same')
        return data['password_2']
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_2'])
        if commit:
            user.save()
        return user
    

class ChangeUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','username']
        
    def clean_pass(self):
        password = ReadOnlyPasswordHashField()
        return self.initial['password']
    
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.search(r'\.(com|net|org|edu)$', email, re.IGNORECASE):
            raise forms.ValidationError("Email must end with .com, .net, .org, or .edu")
        return email
    
    def clean_password(self):
        data = self.cleaned_data
        if not data['password']:
            raise forms.ValidationError('password field are empty')
        if len(data['password']) < 8:
            raise forms.ValidationError('password must be at least 8 charecters')
        return data['password']

class UserRegisterCodeForm(forms.Form):
    code1 = forms.IntegerField(min_value=0, max_value=9)
    code2 = forms.IntegerField(min_value=0, max_value=9)
    code3 = forms.IntegerField(min_value=0, max_value=9)
    code4 = forms.IntegerField(min_value=0, max_value=9)
    code5 = forms.IntegerField(min_value=0, max_value=9)
    code6 = forms.IntegerField(min_value=0, max_value=9)

    def clean(self):
        cleaned_data = super().clean()
        # Combine the six digits into a single string
        code_str = ''.join(str(cleaned_data.get(f'code{i}', '')) for i in range(1, 7))
        
        # Validate length and content
        if len(code_str) != 6 or not code_str.isdigit():
            raise ValidationError("Verification code must be 6 digits.")

        # Add combined code to cleaned_data
        cleaned_data['code'] = int(code_str)
        return cleaned_data
    
class UserEditEmailForm(forms.Form):
    email = forms.EmailField()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        if not re.search(r'\.(com|net|org|edu)$', email, re.IGNORECASE):
            raise forms.ValidationError("Email must end with .com, .net, .org, or .edu")
        return email
    
class ForgotPasswordEmailForm(forms.Form):
    email = forms.EmailField()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.search(r'\.(com|net|org|edu)$', email, re.IGNORECASE):
            raise forms.ValidationError("Email must end with .com, .net, .org, or .edu")
        return email
    
class ForgotPasswordCodeForm(forms.Form):
    code = forms.IntegerField()

class ForgotPasswordSetForm(forms.Form):
    password_1 = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password_2(self):
        data = self.cleaned_data
        if not data['password_1'] or not data['password_2']:
            raise forms.ValidationError('password field are empty')
        if len(data['password_2']) < 8:
            raise forms.ValidationError('password must be at least 8 charecters')        
        if data['password_2'] != data['password_1']:
            raise forms.ValidationError('passwords are not the same')
        return data['password_2']
    
class UserAddAdressForm(forms.Form):
    user_name = forms.CharField(max_length=100)
    city = forms.CharField(max_length=50)
    street = forms.CharField(max_length=350)
    number = forms.IntegerField()
