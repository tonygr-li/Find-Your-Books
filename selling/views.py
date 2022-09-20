from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Post, Images
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import PostCreationForm, ImageForm, WantPostCreationForm
from django.forms import modelformset_factory
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from users.models import User

# Create your views here.

#Home page
def home_en(request):
    context = {
        'title': "Home | FindYourBooks",#Text that shows on top, as title, see top of base.html for more info. (<title> tag)
    }
    return render(request, 'selling/home.html', context)

#Search page
def Search(request):
    search_post = request.GET.get('search', '')
    request.session['search_post'] = search_post #Enregistrement du variable search_post pour réutiliser plus tard pour search par ordre différent
    if search_post:#if there is a search
        posts_list = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).order_by('-date_posted')
        num_results = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).count()
    else:#if there's no search
        posts_list = Post.objects.all().order_by('-date_posted')
        num_results = Post.objects.all().count()

    posts_list_paginator = Paginator(posts_list, 10) #10 posts per page

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = posts_list_paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = posts_list_paginator.page(posts_list_paginator.num_pages)

    context = {
        'posts': posts,
        'result':search_post,
        'num_results':num_results,
        'title': 'Search',
    }
    return render(request, 'selling/search.html', context)

def PriceLowSearch(request):
    search_post = request.session['search_post'] #Get le variable search_post enregistré dans Search
    if search_post:#if there is a search
        posts_list = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).order_by('price')
        num_results = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).count()
    else:#if there's no search
        posts_list = Post.objects.all().order_by('price')
        num_results = Post.objects.all().count()

    posts_list_paginator = Paginator(posts_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = posts_list_paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = posts_list_paginator.page(posts_list_paginator.num_pages)

    context = {
        'posts': posts,
        'result':search_post,
        'num_results':num_results,
        'title':'Search',
    }
    return render(request, 'selling/search.html', context)

def PriceHighSearch(request):
    search_post = request.session['search_post']
    if search_post:#if there is a search
        posts_list = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).order_by('-price')
        num_results = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).count()
    else:#if there's no search
        posts_list = Post.objects.all().order_by('-price')
        num_results = Post.objects.all().count()

    posts_list_paginator = Paginator(posts_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = posts_list_paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = posts_list_paginator.page(posts_list_paginator.num_pages)

    context = {
        'posts': posts,
        'result':search_post,
        'num_results':num_results,
        'title': 'Search',
    }
    return render(request, 'selling/search.html', context)

def DateOldSearch(request):
    search_post = request.session['search_post']
    if search_post:#if there is a search
        posts_list = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).order_by('date_posted')
        num_results = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).count()
    else:#if there's no search
        posts_list = Post.objects.all().order_by('date_posted')
        num_results = Post.objects.all().count()

    posts_list_paginator = Paginator(posts_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = posts_list_paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = posts_list_paginator.page(posts_list_paginator.num_pages)

    context = {
        'posts': posts,
        'result':search_post,
        'num_results':num_results,
        'title': 'Search',
    }
    return render(request, 'selling/search.html', context)

def SearchOffer(request):
    search_post = request.session['search_post']
    if search_post:#if there is a search
        posts_list = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).filter(sell=True).order_by('-date_posted')
        num_results = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).filter(sell=True).count()
    else:#if there's no search
        posts_list = Post.objects.all().filter(sell=True).order_by('-date_posted')
        num_results = Post.objects.all().filter(sell=True).count()

    posts_list_paginator = Paginator(posts_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = posts_list_paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = posts_list_paginator.page(posts_list_paginator.num_pages)

    context = {
        'posts': posts,
        'result':search_post,
        'num_results':num_results,
        'title': 'Search',
    }
    return render(request, 'selling/search.html', context)

def SearchWant(request):
    search_post = request.session['search_post']
    if search_post:#if there is a search
        posts_list = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).filter(sell=False).order_by('-date_posted')
        num_results = Post.objects.all().filter(Q(isbn__icontains=search_post)|Q(title__icontains=search_post)|Q(description__icontains=search_post)).filter(sell=False).count()
    else:#if there's no search
        posts_list = Post.objects.all().filter(sell=False).order_by('-date_posted')
        num_results = Post.objects.all().filter(sell=False).count()

    posts_list_paginator = Paginator(posts_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = posts_list_paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = posts_list_paginator.page(posts_list_paginator.num_pages)

    context = {
        'posts': posts,
        'result':search_post,
        'num_results':num_results,
        'title': 'Search',
    }
    return render(request, 'selling/search.html', context)

#When click on post in search page
def PostInfo(request, pk):
    info = get_object_or_404(Post,pk=pk)
    img_carousel_extra = Images.objects.filter(post__pk=pk)

    context = {
        'info':info,
        'img_carousel_extra': img_carousel_extra,
        'title': 'Post',
    }

    return render(request, 'selling/post_info.html', context)

def PostAuthorProfile(request, pk):
    author_info = get_object_or_404(User, pk=pk)
    items_list = Post.objects.all().filter(author=author_info)
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

    context = {
        'author_info': author_info,
        'posts':items,
        'num_results':num_results,
        'title': 'Post Author Profile',
    }

    return render(request, 'selling/post_author.html', context)

#Sell page
@login_required
def CreatePost(request):
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=4)
    num_posts = Post.objects.filter(author=request.user).count()

    if num_posts < 50: # Max number of posts per user is 50
        if request.method == 'POST':

            postForm = PostCreationForm(request.POST, request.FILES)
            formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

            if postForm.is_valid() and formset.is_valid():
                postForm.instance.author = request.user
                post_form = postForm.save(commit=False)
                post_form.save()

                for form in formset.cleaned_data:
                    # this helps to not crash if the user does not upload all the photos
                    if form:
                        image = form['image']
                        photo = Images(post=post_form, image=image)
                        photo.save()
                # using django messages framework
                messages.success(request,"Your item has been posted!")
                return redirect('sell-home')
            else:
                print(postForm.errors, formset.errors)

        else:
            postForm = PostCreationForm()
            formset = ImageFormSet(queryset=Images.objects.none())

    else:
        return render(request,'selling/max_post.html') # If the user has reached the limit of posts, show max_post html

    return render(request, 'selling/sell.html', {'postForm': postForm, 'formset': formset, 'title':'Create Post'})

#Want page
@login_required
def WantCreatePost(request):
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=4)
    num_posts = Post.objects.filter(author=request.user).count()

    if num_posts < 50: # Max number of posts per user is 50
        if request.method == 'POST':

            postForm = WantPostCreationForm(request.POST, request.FILES)
            formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

            if postForm.is_valid() and formset.is_valid():
                postForm.instance.author = request.user
                postForm.instance.sell = False
                post_form = postForm.save(commit=False)
                post_form.save()

                for form in formset.cleaned_data:
                    # this helps to not crash if the user does not upload all the photos
                    if form:
                        image = form['image']
                        photo = Images(post=post_form, image=image)
                        photo.save()
                # using django messages framework
                messages.success(request,"Your item has been posted!")
                return redirect('sell-home')
            else:
                print(postForm.errors, formset.errors)

        else:
            postForm = WantPostCreationForm()
            formset = ImageFormSet(queryset=Images.objects.none())
    else:
        return render(request,'selling/max_post.html') # If the user has reached the limit of posts, show max_post html

    return render(request, 'selling/want.html', {'postForm': postForm, 'formset': formset, 'title':'Create Post'})

@login_required()
def UpdatePostAddImages(request, pk):
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=4)
    item_add_img = Images.objects.filter(post__pk=pk)
    post_author = Post.objects.get(pk=pk).author

    if request.user == post_author:
        if request.method == 'POST':
            formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none(), instance=item_add_img)

            if formset.is_valid():

                for form in formset.cleaned_data:
                    # this helps to not crash if the user does not upload all the photos
                    if form:
                        image = form['image']
                        photo = Images(image=image)
                        photo.save()
                # using django messages framework
                messages.success(request, "Your images have been updated!")
                return redirect('sell-home')
            else:
                print(formset.errors)

        else:
            formset = ImageFormSet(queryset=Images.objects.none())
        return render(request, 'selling/edit_img.html', {'formset': formset, 'title':"Update Images"})

    else:
        return HttpResponseForbidden()






class EditPost(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreationForm
    template_name="selling/update-post.html"
    success_message = 'Your item has been updated!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_message = 'Your item has been deleted'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False