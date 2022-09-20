from django import forms
from users.models import User, ReportUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Mot de passe:', widget=forms.PasswordInput(
        attrs={'class': 'form-control mt-2'})
    )
    password2 = forms.CharField(label='Confirmer le mot de passe:', widget=forms.PasswordInput(
        attrs={'class': 'form-control mt-2'})
    )
    email = forms.EmailField(label='Courriel', widget=forms.EmailInput(attrs={'class': 'form-control mt-2'}))
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class':'form-control mt-2'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(
        attrs={'class': 'form-control mt-2'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control mt-2',
        }
))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Courriel", widget=forms.EmailInput(attrs={'class': 'form-control mt-2'}))
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control mt-2'}))

    class Meta:
        model = User
        fields = ['username', 'email']

class ReportForm(forms.ModelForm):

    REPORT_CHOICES = [
        ('other', "-- Sélectionner --"),
        ('inappropriate', 'Elle contient du langage et/ou du contenu offensif et/ou inapproprié.'),
        ('spam', "C'est du spam"),
        ('laws', "Il ne conforme pas aux lois"),
        ('false_info', 'Elle contient de la fausse information'),
        ('irrelevant', "Elle n'a pas rapport"),
        ('other', 'Autre'),
    ]

    category = forms.CharField(widget=forms.Select(
        attrs={'class':'form-control mt-2'},choices=REPORT_CHOICES,
    ))

    class Meta:
        model=ReportUser
        fields = ['category']

class ResendActivationEmail(forms.ModelForm):

    email = forms.EmailField(label="Courriel", widget=forms.EmailInput(attrs={'class': 'form-control mt-2'}))

    class Meta:
        model = User
        fields = ['email']