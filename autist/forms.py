# -*- coding: utf-8 -*-
from .models import Post, AddProject, VkPosts, FbPosts, TwPosts, OkPosts, InPosts
from django import forms
from allauth.socialaccount.models import SocialAccount



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class ContactForm (forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(max_length=2000, widget=forms.Textarea, required=True)


class AddProjectForm(forms.ModelForm):
    accounts = forms.ModelMultipleChoiceField(queryset=SocialAccount.objects.all(),
                                     widget=forms.CheckboxSelectMultiple,
                                     required=True)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.accounts = SocialAccount.objects.filter(user=self.request.user)
        super(AddProjectForm, self).__init__(*args, **kwargs)
        self.fields['accounts'].queryset = self.accounts

    class Meta:
        model = AddProject
        fields = ('title', 'accounts',)

class VkPostsForm(forms.ModelForm):
    class Meta:
        model = VkPosts
        fields = ('text',)

class FbPostsForm(forms.ModelForm):
    class Meta:
        model = FbPosts
        fields = ('text',)

class TwPostsForm(forms.ModelForm):
    class Meta:
        model = TwPosts
        fields = ('text',)

class OkPostsForm(forms.ModelForm):
    class Meta:
        model = OkPosts
        fields = ('text',)

class InPostsForm(forms.ModelForm):
    class Meta:
        model = InPosts
        fields = ('text',)
