# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.shortcuts import redirect
from messages.forms import *
from django.views.static import serve
from django.conf import settings

@login_required(login_url='/account/login/')
def hello(request):
    t = loader.get_template("index.html")
    c = RequestContext(request)
    return HttpResponse(t.render(c))

def login_form(request):
    t = loader.get_template("login.html")
    c = RequestContext(request)
    return HttpResponse(t.render(c))

@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            return redirect('account/login/')
    else:
        raise Http404

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/account/login/')
def send(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.creator = request.user
            report.save()
            form.save_m2m()

            formset = ReportFileFormSet(request.POST, request.FILES, instance=report)
            if formset.is_valid():
                formset.save()
            else:
                raise Http404
        return redirect('/')
    else:
        raise Http404

@login_required(login_url='/account/login/')
def save(request,id):
    if request.method == 'POST':
        rep = Report.objects.get(pk=id)
        form = ReportForm(request.POST, instance=rep)
        if form.is_valid():
            form.save()
            formset = ReportFileFormSet(request.POST, request.FILES, instance=rep)
            if formset.is_valid():
                formset.save()
        return redirect('/report/'+id+'/')
    else:
        raise  Http404

@login_required(login_url='/account/login/')
def account_change_form(request):
    t = loader.get_template("change_password.html")
    c = RequestContext(request)
    return HttpResponse(t.render(c))

@login_required(login_url='/account/login/')
def account_change(request):
    alert = 1
    if request.method == 'POST':
        op = request.POST['old_pass']
        np = request.POST['new_pass']
        cp = request.POST['con_pass']

        if not request.user.check_password(op):
            alert = 3
        if (np != cp) or (np == '' and cp == ''):
            alert = 2
        if alert == 1:
            request.user.set_password(np)
            request.user.save()
            t = loader.get_template("change_password.html")
            c = RequestContext(request,{'msg':alert,})
            return HttpResponse(t.render(c))
        else:
            t = loader.get_template("change_password.html")
            c = RequestContext(request,{'msg':alert,})
            return HttpResponse(t.render(c))
    else:
        raise Http404

def mediaserver(request, path):
    return serve(request, path, settings.MEDIA_ROOT)