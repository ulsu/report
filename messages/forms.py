# -*- coding: utf-8 -*-
from django import forms
from models import *
from django.forms.models import inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ['creator','creation_date']

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user', None)
        super(ReportForm, self).__init__(*args, **kwargs)

        self.fields["viewers"].widget = CheckboxSelectMultiple()

        queryset = User.objects.filter(is_superuser=False, is_secretary=False)
        if self.user is not None:
            queryset = queryset.exclude(id=self.user.id)

        self.fields["viewers"].queryset = queryset
        self.fields["viewers"].help_text = ''
        self.fields['title'].widget.attrs["class"] = 'form-control'
        self.fields['text'].widget.attrs["class"] = 'form-control'


class ReportFileForm(forms.ModelForm):
    class Meta:
        model = ReportFile
        exclude = ['report']

ReportFileFormSet = inlineformset_factory(Report, ReportFile, form=ReportFileForm, extra=1)