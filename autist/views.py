# -*- coding: utf-8 -*-
from django.utils import timezone
from .models import Post, AddProject
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from allauth.socialaccount.forms import DisconnectForm
from .forms import ContactForm, AddProjectForm, VkPostsForm
from allauth.account.views import (
    AjaxCapableProcessFormViewMixin,
    CloseableSignupMixin,
    RedirectAuthenticatedUserMixin,
)
from django.views.generic.edit import FormView
from allauth.compat import reverse, reverse_lazy
from allauth.utils import get_form_class
from allauth.socialaccount import app_settings, helpers
from allauth.account.adapter import get_adapter as get_account_adapter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.account import app_settings as account_settings
from allauth.socialaccount.models import SocialToken
import vk



class ConnectionsView(AjaxCapableProcessFormViewMixin, FormView):
    template_name = (
        "adminlte/index."  +
        account_settings.TEMPLATE_EXTENSION)
    form_class = AddProjectForm
    success_url = reverse_lazy("projects")

    def get_form_class(self):
        return get_form_class(app_settings.FORMS,
                              'account_list',
                              self.form_class)

    def get_form_kwargs(self):
        kwargs = super(ConnectionsView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        get_account_adapter().add_message(self.request,
                                          messages.INFO,
                                          'socialaccount/messages/'
                                          'account_disconnected.txt')
        form.save()
        return super(ConnectionsView, self).form_valid(form)

    def get_ajax_data(self):
        account_data = []
        for account in SocialAccount.objects.filter(user=self.request.user):
            provider_account = account.get_provider_account()
            account_data.append({
                'id': account.pk,
                'provider': account.provider,
                'name': provider_account.to_str()
            })
        return {
            'projects': account_data
        }

connections = login_required(ConnectionsView.as_view())

def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
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
    access_token = SocialToken.objects.filter(account__user=request.user, account__provider='vk')
    session = vk.Session(access_token=access_token)
    api = vk.API(session)
    api.wall.post(scope='wall', message='Hello, World!')
    if request.method == "POST":
        form = VkPostsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_in_vk')
    else:
        form = VkPostsForm()
    return render(request, 'adminlte/post_in_vk.html', {'form': form, 'access_token': access_token})














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