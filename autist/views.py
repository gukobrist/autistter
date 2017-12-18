# -*- coding: utf-8 -*-
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date') #собираем все посты
    
    paginator = Paginator(posts, 10) # на странице будет по 10 постов

    page = request.GET.get('page')
    try:
		# Если существует, то выбираем эту страницу
        post = paginator.page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        post = paginator.page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
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

def page_about(request):
    return render(request, 'autist/about.html');

def page_contact(request):
    return render(request, 'autist/contact.html');

