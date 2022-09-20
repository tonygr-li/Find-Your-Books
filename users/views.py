from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, ReportForm, UserUpdateForm, ResendActivationEmail
from .models import *
from django.contrib.auth.decorators import login_required
from selling.models import Post
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.sites.shortcuts import  get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from .decorators import allowed_users
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
    email_subject = 'Activate Your Account To Start Selling Books'
    email_body = render_to_string('users/activate.html', {
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
            'title':'Register',
        }

        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 6:
            messages.add_message(request, messages.ERROR,
                                 'Password should contain at least 6 characters')
            context['has_error'] = True

        if password1 != password2:
            messages.add_message(request, messages.ERROR,
                                 "Passwords don't match")
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Username is taken, please choose another one')
            context['has_error'] = True

            return render(request, 'users/register.html', context, status=409)

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Email is taken, please choose another one')
            context['has_error'] = True

            return render(request, 'users/register.html', context, status=409)

        if context['has_error']:
            return render(request, 'users/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password1)
        user.save()

        if not context['has_error']:
            send_activation_email(user, request)

            messages.add_message(request, messages.SUCCESS,
                                 "We sent you an email to verify your account. Please check your spam folder if you don't find the email.")
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form':form})

def resend_activate_email(request):
    if request.method == 'POST':
        form = ResendActivationEmail(request.POST)

        context = {
            'has_error': False,
            'data': request.POST,
            'form': form,
            'title':'Resend Activation Email',
        }

        email = request.POST.get('email')

        if User.objects.filter(email=email).count() == 0:
            messages.add_message(request, messages.ERROR, "Account with this email doesn't exist. Please register to create an account.")
            context['has_error'] = True

            return render(request, 'users/resend_activate_email.html', context, status=409)


        if not context['has_error']:
            user = get_object_or_404(User, email=email)

            send_activation_email(user, request)

            messages.add_message(request, messages.SUCCESS,
                                 "We sent you an email to verify your account. Please check your spam folder if you don't find the email.")
            return redirect('login')

    else:
        form = ResendActivationEmail()

    return render(request, 'users/resend_activate_email.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        context = {
            'data': request.POST,
            'form':form,
            'title':'Login',
        }
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and not user.is_email_verified: # Check if email is verified
            messages.add_message(request, messages.ERROR, 'Email is not verified, please check your email inbox')
            return render(request, 'users/login.html', context, status=401)

        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Invalid username or password, try again')
            return render(request, 'users/login.html', context, status=401)

        login(request, user)

        messages.add_message(request, messages.SUCCESS,
                             f'Log in successful for user {user.username}')

        return redirect(reverse('sell-home'), {'form':form})

    else:
        form=UserLoginForm()

    return render(request, 'users/login.html', {'form':form})

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
                             'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'users/activate_failed.html', {"user": user, 'title': 'Activate User'})

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
        'title':'Profile',
    }
    return render(request, 'users/profile.html', context)

@login_required()
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form':form,
        'title':'Update Profile',
    }

    return render(request,'users/update_profile.html', context)

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
                'title':'Report User',
            }

            if form.is_valid():
                form.instance.reported = reported
                form.instance.reporting = reporting
                form.save()
                messages.success(request,f"You have successfully reported {reported.author.username}")
                return redirect('sell-home')
        else:
            form = ReportForm()

            context = {
                'form':form,
                'title':'Report User',
            }

        return render(request, 'users/report_user.html', context)
        #ReportUser_instance = ReportUser.objects.create(reporting=reporting, reported=reported)

        #ReportUser_instance.save()

    else:

        context = {
            'reported':reported,
            'title':'Report User',
        }

        return render(request, 'users/already_reported.html', context)

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

    return render(request,'users/admin_page.html', context)

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
        'title':'Report List',
    }

    return render(request,'users/report_list.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def report_info(request, pk):
    items = ReportUser.objects.filter(reported__author__pk = pk)
    first_item = items.first()

    context = {
        'items':items,
        'first_item':first_item,
        'title':'Report Info',
    }

    return render(request, 'users/report_info.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def dismiss_report(request, pk):
    items = ReportUser.objects.filter(reported__author__pk = pk)
    items.delete()
    return redirect('report-leaders')

def unauthorized(request):
    context = {
        'title':'Unauthorized'
    }
    return render(request, 'users/not_authorized.html', context)

def guide(request):
    context = {
        'title':'Guide'
    }
    return render(request, 'users/guide.html', context)

def terms(request):
    context = {
        'title':'Terms of Use'
    }
    return render(request, 'users/terms_of_use.html', context)

def about(request):
    context = {
        'title':'About'
    }
    return render(request, 'users/about.html', context)

def handler404(request, exception):
    context = {'title':'404'}
    response = render(request, "users/404.html", context=context)
    response.status_code = 404
    return response

def handler500(request, exception=None):
    context = {'title':'500'}
    response = render(request, "users/500.html", context=context)
    response.status_code = 500
    return response

def handler403(request, exception=None):
    context = {'title':'403'}
    response = render(request, "users/403.html", context=context)
    response.status_code = 403
    return response

def handler400(request, exception=None):
    context = {'title':'400'}
    response = render(request, "users/400.html", context=context)
    response.status_code = 400
    return response