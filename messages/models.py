# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from datetime import datetime
from main.models import User

class Report(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(blank=True, null=True,verbose_name='Описание')
    creation_date = models.DateTimeField(default=datetime.now())
    creator = models.ForeignKey(User, related_name='my_reports')
    viewers = models.ManyToManyField(User, related_name='reports',verbose_name='Пользователи',null=True,blank=True)

    class Meta:
        ordering = ('creation_date','title','text',)

    def __unicode__(self):
        return self.title

    def comments(self):
        return self._comments.filter(parent=None)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('title','text','creation_date','creator',)
admin.site.register(Report, ReportAdmin)


class ReportFile(models.Model):
    report = models.ForeignKey(Report, related_name='attachments')

    def upload_path(self, filename):
        return 'reports/%s/%s' % (self.report.id, filename)

    media_file = models.FileField(upload_to=upload_path)
    is_infected = models.BooleanField(default=False,verbose_name='Вредоносный')


class ReportFileAdmin(admin.ModelAdmin):
        list_display = ('report','media_file','is_infected',)
admin.site.register(ReportFile, ReportFileAdmin)

class Comment(models.Model):
    report = models.ForeignKey(Report, related_name='_comments')
    parent = models.ForeignKey('Comment', related_name='children', blank=True, null=True)
    text = models.TextField()
    creation_date = models.DateTimeField(default=datetime.now())
    author = models.ForeignKey(User,related_name='comments')

    def __unicode__(self):
        return '%s - %s (%s)' % (self.author.username, self.report.title, self.creation_date)

class CommentAdmin(admin.ModelAdmin):
        list_display = ('text','author','creation_date','parent','report',)
admin.site.register(Comment, CommentAdmin)


