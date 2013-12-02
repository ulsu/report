# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.core import validators
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
import re

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
                                ])
    email = models.EmailField(_('email address'), max_length=254, blank=True)
    is_staff = models.BooleanField('Статус администратора', default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    is_secretary = models.BooleanField('Статус персонала', default=False,
                                       help_text='Отметьте, если пользователь обладает модераторскими правами.')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        username = self.username
        return username.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.username.strip()

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
