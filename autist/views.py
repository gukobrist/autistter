# -*- coding: utf-8 -*-
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from allauth.account.utils import send_email_confirmation
from braces.views import LoginRequiredMixin
from .models import UserProfile
from .forms import IdentiteForm, EmailForm

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


class ProfileHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'userprofiles/home.html'
    user_check_failure_path = '/comptes/signup/'

    def check_user(self, user):
        if user.is_active:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ProfileHomeView, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get_or_create(user=self.request.user)[0]
        context['profile'] = profile
        return context


class ProfileIdentite(LoginRequiredMixin, UpdateView):
    template_name = "userprofiles/identity_form.html"
    form_class = IdentiteForm
    user_check_failure_path = '/comptes/login/'
    success_url = reverse_lazy("profile-home")

    def get_queryset(self):
        queryset = UserProfile.objects.filter(user=self.request.user)
        return queryset

    def form_valid(self, form, **kwargs):
        profile = form.save(commit=False)
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        profile.gender = form.cleaned_data['gender']
        profile.phone = form.cleaned_data['phone']
        profile.personal_info_is_completed = True
        profile.completion_level = profile.get_completion_level()
        profile.save()
        # return super(ProfileIdentite, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())