# -*- coding: utf-8 -*-
from django.utils import timezone
from .models import Post, AddProject
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from allauth.socialaccount.forms import DisconnectForm
from .forms import ContactForm, AddProjectForm, VkPostsForm, FbPostsForm, TwPostsForm, OkPostsForm, InPostsForm
from allauth.socialaccount.models import SocialToken
from taggit.models import Tag
import vk
import tweepy


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request, 'autist/post_list.html', {'posts': post})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'autist/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.pk)
    else:
        form = PostForm()
    return render(request, 'autist/post_edit.html', {'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'autist/post_edit.html', {'form': form})

def page_add_project(request):
    project = AddProject.objects.filter(user=request.user)
    if request.method == "POST":
        form = AddProjectForm(request.POST, request=request)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            for c in request.POST.getlist('accounts'):
                project.accounts.add(c)
            project.save()
            return redirect('projects')
    else:
        form = AddProjectForm(request=request)
    return render(request, 'adminlte/project.html', {'form': form, 'project': project})

def page_edit_project(request, pk):
    project = get_object_or_404(AddProject, pk=pk)
    if request.method == "POST":
        form = AddProjectForm(request.POST, instance=project,  request=request)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            form.save_m2m()
            return redirect('projects')
    else:
        form = AddProjectForm(instance=project,  request=request)
    return render(request, 'adminlte/project_edit.html', {'form': form})

def project_delete(request, pk):
    project_delete = get_object_or_404(AddProject, pk=pk).delete()
    return redirect('projects')

def post_in_vk(request):
    access_token1 = '86073c41248a49aeb0beb58269ece553d0a96550f58a7375859994a937f119241e0f0b269848cd75caba4'
    access_token = SocialToken.objects.filter(account__user=request.user, account__provider='vk')
    session = vk.Session(access_token=access_token)
    api = vk.API(session)
    if request.method == "POST":
        form = VkPostsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            api.wall.post(message=post.text)
            post.save()
            return redirect('post_in_vk')
    else:
        form = VkPostsForm()
    return render(request, 'adminlte/post_in_vk.html', {'form': form, 'access_token': access_token})

def post_in_fb(request):
    access_token = SocialToken.objects.filter(account__user=request.user, account__provider='facebook')
    if request.method == "POST":
        form = FbPostsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_in_fb')
    else:
        form = FbPostsForm()
    return render(request, 'adminlte/post_in_fb.html', {'form': form, 'access_token': access_token})

def post_in_tw(request):
    access_token1 = SocialToken.objects.filter(account__user=request.user, account__provider='twitter')
    consumer_key = "vn4gp37PepEl6y7EF2Vusz16N"
    consumer_secret = "2lTkAMihPNH1JiOBIX7TvYVVDE26wTdnubtIvwt5d0LCJA2ClF"
    access_token = "2435169787-n57nhrh3xC6SS7n7z16WQJ6NAXESvuCNXbasnYK"
    access_token_secret = "nwMB5aYJTp7WeDsTatc3N5aiP9lm1F4BgETuHtvVNjkDS"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    if request.method == "POST":
        form = TwPostsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            api.update_status(post.text)
            post.save()
            return redirect('post_in_tw')
    else:
        form = TwPostsForm()
    return render(request, 'adminlte/post_in_tw.html', {'form': form, 'access_token': access_token})

def post_in_ok(request):
    access_token = SocialToken.objects.filter(account__user=request.user, account__provider='odnoklassniki')
    if request.method == "POST":
        form = OkPostsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_in_ok')
    else:
        form = OkPostsForm()
    return render(request, 'adminlte/post_in_ok.html', {'form': form, 'access_token': access_token})

def post_in_in(request):
    access_token = SocialToken.objects.filter(account__user=request.user, account__provider='instagram')
    if request.method == "POST":
        form = InPostsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_in_in')
    else:
        form = InPostsForm()
    return render(request, 'adminlte/post_in_in.html', {'form': form, 'access_token': access_token})














def page_contact(request):
    form = ContactForm(request.POST)
    if request.recaptcha_is_valid:
        pass
    return render(request, 'autist/contact.html', {'form': form})

def page_about(request):
    return render(request, 'autist/about.html')

def dashboard(request):
    return render(request, 'adminlte/index.html')

def page_example(request):
    return render(request, 'adminlte/example.html')

def page_connect_accounts(request):
    myform = DisconnectForm(request=request)
    return render(request, 'adminlte/connect.html', {"form": myform})