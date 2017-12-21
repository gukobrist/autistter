# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import hashlib
from allauth.socialaccount.models import SocialAccount


GENDER =(('мужчина','Мужчина'),('женщина','Женщина'),('трап','Трап'))


class UserProfile(models.Model):  
    user = models.OneToOneField(User, null=True, related_name="profile", verbose_name=_(u'User'))
    phone = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u"Телефон"))
    gender = models.CharField(max_length=40, blank=True, verbose_name=_(u'Пол'), choices=GENDER)
    avatar = models.ImageField(upload_to='userprofiles/avatars', null=True, blank=True, verbose_name=_(u"Аватар"))
    completion_level = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'Процент заполнения профиля'))
    email_is_verified = models.BooleanField(default=False, verbose_name=_(u'Email верифицирован'))
    personal_info_is_completed = models.BooleanField(default=False, verbose_name=_(u'Персональная информация заполнена'))

    class Meta:
        verbose_name=_(u'User profile')
        verbose_name_plural = _(u'User profiles')
        
    def __unicode__(self):
        return u"User profile: %s" % self.user.username
    
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

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email.encode('utf-8')).hexdigest())

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])