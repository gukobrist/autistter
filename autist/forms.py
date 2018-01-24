# -*- coding: utf-8 -*-
from django import forms
from .models import Post, AddProject
from phonenumber_field.modelfields import PhoneNumberField
from django import forms
from allauth.socialaccount.models import SocialAccount


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class ContactForm (forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    phone = PhoneNumberField(max_length=30)
    message = forms.CharField(max_length=2000, widget=forms.Textarea(), help_text='Напиши мне')
    source = forms.CharField(max_length=50, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')

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



