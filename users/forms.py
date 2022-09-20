from django import forms
from .models import User, ReportUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password:', widget=forms.PasswordInput(
        attrs={'class': 'form-control mt-2'})
    )
    password2 = forms.CharField(label='Confirm password:', widget=forms.PasswordInput(
        attrs={'class': 'form-control mt-2'})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mt-2'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mt-2'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control mt-2',
        }
))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mt-2'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mt-2'}))

    class Meta:
        model = User
        fields = ['username', 'email']

class ReportForm(forms.ModelForm):

    REPORT_CHOICES = [
        ('other', "-- Select --"),
        ('inappropriate', 'It contains offensive and/or inappropriate language and/or content.'),
        ('spam', 'It is spam'),
        ('laws', "It doesn't conform to laws"),
        ('false_info', 'It contains false information'),
        ('irrelevant', 'It is irrelevant'),
        ('other', 'Other'),
    ]

    category = forms.CharField(widget=forms.Select(
        attrs={'class':'form-control mt-2'},choices=REPORT_CHOICES,
    ))

    class Meta:
        model=ReportUser
        fields = ['category']

class ResendActivationEmail(forms.ModelForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mt-2'}))

    class Meta:
        model = User
        fields = ['email']