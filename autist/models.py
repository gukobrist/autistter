# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from uuslug import slugify
from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib
from django.utils.translation import ugettext_lazy as _

GENDER =(('мужчина','Мужчина'),('женщина','Женщина'), ('трап','Трап'))

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    slug = models.CharField(verbose_name='Транслит', max_length=200, blank=True)  # Поле для записи ссылки
    text = RichTextUploadingField(blank=True, default='')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    seo_title = models.CharField('Title', blank=True, max_length=250)
    seo_description = models.CharField('Description', blank=True, max_length=250)
    seo_keywords = models.CharField('Keywords', blank=True, max_length=250)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def save(self):
        self.slug = '{0}-{1}'.format(self.pk, slugify(self.title))  # Статья будет отображаться в виде NN-АА-АААА
        super(Post, self).save()


# модель профиля для отображения информации об авторизированном профиле
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, related_name="profile", verbose_name=_(u'User'))
    phone = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=40, blank=True, verbose_name=_(u'Gender'), choices=GENDER)
    avatar = models.ImageField(upload_to='userprofiles/avatars', null=True, blank=True, verbose_name=_(u"Avatar"))
    completion_level = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'Profile completion percentage'))
    email_is_verified = models.BooleanField(default=False, verbose_name=_(u'Email is verified'))
    personal_info_is_completed = models.BooleanField(default=False, verbose_name=_(u'Personal info completed'))

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    def get_completion_level(self):
        completion_level = 0
        if self.email_is_verified:
            completion_level += 50
        if self.personal_info_is_completed:
            completion_level += 50
        return completion_level

    def update_completion_level(self):
        self.completion_level = self.get_completion_level()
        self.save()
        return

    class Meta:
        db_table =_(u'User profile')
        verbose_name =_(u'User profile')
        verbose_name_plural =_(u'User profiles')

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email.encode('utf-8')).hexdigest())


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

#модель поста в соцсети


