from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, ReportForm, UserUpdateForm, ResendActivationEmail
from users.models import *
from django.contrib.auth.decorators import login_required
from selling.models import Post
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.sites.shortcuts import  get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from users.utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from users.decorators import allowed_users
from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, InvalidPage

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# See video: https://www.youtube.com/watch?v=Rbkc-0rqSw8 for more details on email activation
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Active ton compte pour commencer à vendre des livres'
    email_body = render_to_string('utilisateurs/activate.html', {
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email=EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])

    EmailThread(email).start()

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        context = {
            'has_error': False,
            'data': request.POST,
            'form':form,
            'title':"S'inscrire",
        }

        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 6:
            messages.add_message(request, messages.ERROR,
                                 'Le mot de passe doit contenir au moins 6 caractères')
            context['has_error'] = True

        if password1 != password2:
            messages.add_message(request, messages.ERROR,
                                 "Les mots de passe sont différents")
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR,
                                 "Le nom d'utilisateur est requis")
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 "Le nom d'utilisateur est déjà pris. Veuillez en prendre un autre")
            context['has_error'] = True

            return render(request, 'utilisateurs/register.html', context, status=409)

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Le courriel est déjà pris. Veuillez en prendre un autre')
            context['has_error'] = True

            return render(request, 'utilisateurs/register.html', context, status=409)

        if context['has_error']:
            return render(request, 'utilisateurs/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password1)
        user.save()

        if not context['has_error']:
            send_activation_email(user, request)

            messages.add_message(request, messages.SUCCESS,
                                 "Nous vous avons envoyé un courriel pour vérifier votre compte. Veuillez consulter votre dosser spam si vous ne trouvez pas le courriel")
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'utilisateurs/register.html', {'form':form})

def resend_activate_email(request):
    if request.method == 'POST':
        form = ResendActivationEmail(request.POST)

        context = {
            'has_error': False,
            'data': request.POST,
            'form': form,
            'title':"Renvoyer le courriel d'activation",
        }

        email = request.POST.get('email')

        if User.objects.filter(email=email).count() == 0:
            messages.add_message(request, messages.ERROR, "Un compte avec ce courriel n'existe pas. Veuillez vous inscrire pour créer un compte.")
            context['has_error'] = True

            return render(request, 'utilisateurs/resend_activate_email.html', context, status=409)


        if not context['has_error']:
            user = get_object_or_404(User, email=email)

            send_activation_email(user, request)

            messages.add_message(request, messages.SUCCESS,
                                 "Nous vous avons envoyé un courriel pour vérifier votre compte. Veuillez consulter votre dosser spam si vous ne trouvez pas le courriel.")
            return redirect('login')

    else:
        form = ResendActivationEmail()

    return render(request, 'utilisateurs/resend_activate_email.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        context = {
            'data': request.POST,
            'form':form,
            'title':'Connexion',
        }
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and not user.is_email_verified: # Check if email is verified
            messages.add_message(request, messages.ERROR, "Votre courriel n'est pas vérifié. Veuillez consulter votre courriel.")
            return render(request, 'utilisateurs/login.html', context, status=401)

        if not user:
            messages.add_message(request, messages.ERROR,
                                 "Nom d'utilisateur ou mot de passe invalide. Veuillez réessayer.")
            return render(request, 'utilisateurs/login.html', context, status=401)

        login(request, user)

        messages.add_message(request, messages.SUCCESS,
                             f"Connexion réussie pour l'utilisateur {user.username}")

        return redirect(reverse('sell-home'), {'form':form})

    else:
        form=UserLoginForm()

    return render(request, 'utilisateurs/login.html', {'form':form})

def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Courriel vérifié. Vous pouvez maintenant vous connecter.')
        return redirect(reverse('login'))

    return render(request, 'utilisateurs/activate_failed.html', {"user": user, 'title': "Activer le compte"})

#User profile
@login_required()
def profile(request):
    items_list = Post.objects.all().filter(author=request.user)
    num_results = items_list.count()

    posts_list_paginator = Paginator(items_list, 10)  # 10 posts per page

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        items = posts_list_paginator.page(page)
    except(EmptyPage, InvalidPage):
        items = posts_list_paginator.page(posts_list_paginator.num_pages)

    context={
        'posts':items,
        'num_results':num_results,
        'title':'Profil',
    }
    return render(request, 'utilisateurs/profile.html', context)

@login_required()
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ton compte a été mis à jour!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form':form,
        'title':'Mettre à jour le profil',
    }

    return render(request,'utilisateurs/update_profile.html', context)

@login_required()
def report_user(request, pk):
    reported = Post.objects.get(pk=pk)
    reporting = request.user


    if ReportUser.objects.filter(reported=reported, reporting=reporting).count() == 0:
        if request.method == 'POST':
            form = ReportForm(request.POST)

            context = {
                'form':form,
                'reported':reported,
                'reporting':reporting,
                'title':'Signaliser un utilisateur',
            }

            if form.is_valid():
                form.instance.reported = reported
                form.instance.reporting = reporting
                form.save()
                messages.success(request,f"Vous avez signalé {reported.author.username} avec succès")
                return redirect('sell-home')
        else:
            form = ReportForm()

            context = {
                'form':form,
                'title':'Signaliser un utilisateur',
            }

        return render(request, 'utilisateurs/report_user.html', context)
        #ReportUser_instance = ReportUser.objects.create(reporting=reporting, reported=reported)

        #ReportUser_instance.save()

    else:

        context = {
            'reported':reported,
            'title':'Signaliser un utilisateur',
        }

        return render(request, 'utilisateurs/already_reported.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def admin_page(request):
    report_leaders = ReportUser.objects.annotate(count=Count('reported__author')).order_by('-count')
    expired_posts = Post.objects.filter(expiry_date__lt=timezone.now())
    post_number = Post.objects.all().count()
    user_number = User.objects.all().count()

    context = {
        'report_leaders': report_leaders,
        'expired_posts':expired_posts,
        'post_number':post_number,
        'user_number':user_number,
        'title':'Staff',
    }

    return render(request,'utilisateurs/admin_page.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def delete_outdated_posts(request):
    expired_posts = Post.objects.filter(expiry_date__lt=timezone.now())
    expired_posts.delete()
    return redirect('staff')

@login_required()
@allowed_users(allowed_roles=['admin'])
def report_leaders(request):
    list = ReportUser.objects.values('reported__author').annotate(count=Count('reported__author')).order_by('-count')
    num_results = list.count()

    list_paginator = Paginator(list, 20)  # 20 items per page

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        list = list_paginator.page(page)
    except(EmptyPage, InvalidPage):
        list = list_paginator.page(list_paginator.num_pages)

    context = {
        'items':list,
        'num_results':num_results,
        'title':'Liste des signalisations',
    }

    return render(request,'utilisateurs/report_list.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def report_info(request, pk):
    items = ReportUser.objects.filter(reported__author__pk = pk)
    first_item = items.first()

    context = {
        'items':items,
        'first_item':first_item,
        'title':'Info sur signalisation',
    }

    return render(request, 'utilisateurs/report_info.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def dismiss_report(request, pk):
    items = ReportUser.objects.filter(reported__author__pk = pk)
    items.delete()
    return redirect('report-leaders')

def unauthorized(request):
    context = {
        'title':'Non autorisé'
    }
    return render(request, 'utilisateurs/not_authorized.html', context)

def guide(request):
    context = {
        'title':'Guide'
    }
    return render(request, 'utilisateurs/guide.html', context)

def terms(request):
    context = {
        'title':"Conditions d'utilisation"
    }
    return render(request, 'utilisateurs/terms_of_use.html', context)

def about(request):
    context = {
        'title':'À propos de nous'
    }
    return render(request, 'utilisateurs/about.html', context)
