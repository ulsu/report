# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from forms import *
from messages.models import *

@login_required(login_url='/account/login/')
def report_create(request):
    form = ReportForm(user=request.user)
    formset = ReportFileFormSet()
    t = loader.get_template("report_form.html")
    c = RequestContext(request,{'form':form, 'formset':formset, })
    return HttpResponse(t.render(c))

@login_required(login_url='/account/login/')
def report_list(request):
    if request.user.is_secretary or request.user.is_superuser:
        rlist = Report.objects.all().order_by("-creation_date")
    else:
        rlist = request.user.reports.all().order_by("-creation_date")
    t = loader.get_template("report_list.html")
    c = RequestContext(request,{'rlist':rlist, })
    return HttpResponse(t.render(c))

@login_required(login_url='/account/login/')
def my_report_list(request):
    mylist = request.user.my_reports.all().order_by("-creation_date")
    t = loader.get_template("mylist.html")
    c = RequestContext(request,{'mylist':mylist, })
    return HttpResponse(t.render(c))

@login_required(login_url='/account/login/')
def report_view(request,id):
    rep = Report.objects.get(pk=id)
    repf = ReportFile.objects.filter(report=rep)
    t = loader.get_template("report.html")
    c = RequestContext(request,{'report':rep, 'files':repf,})
    return HttpResponse(t.render(c))

@login_required(login_url='/account/login/')
def report_edit(request,id):
    rep = Report.objects.get(pk=id)
    form = ReportForm(instance=rep)
    form_id = id
    formset = ReportFileFormSet(instance=rep)
    t = loader.get_template("report_edit.html")
    c = RequestContext(request,{'form':form, 'formset':formset, 'id':form_id })
    return HttpResponse(t.render(c))

@login_required(login_url='/account/login/')
def comment_add(request,id):
    #if request.user.is_superuser
    if request.method == 'POST':
        dict = {
            'text' : request.POST['comment_text'],
            'author' : request.user,
            'report_id' : id,
        }
        Comment.objects.create(**dict)
        return redirect('/report/'+id)
    else:
        raise Http404
