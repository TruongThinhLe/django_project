from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from .form import *
from datetime import datetime,timedelta,date


def index(request):
	return render(request,'index.html')
def english(request):
    form=Word_form()
    form_mean=Form_mean()
    if request.method=='POST':
        if 'submit_newword' in request.POST:
            print(request.POST)
            form = Word_form(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/english')
    current_week=date.today().isocalendar()[1]
    words=English.objects.filter(pub_date__week=current_week)
    context={'words':words,'form':form,'form_mean':form_mean}
    return render(request,'english.html',context)
def plan(request):
    form=Plan_form()
    if request.method=='POST':
        print(request.POST)
        form=Plan_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/plan')
            
    plans=Plan.objects.all()
    rate={}
    for plan in plans :
        plan.status=get_status(plan.date_end,plan.date_start)
        plan.save()
    
    context={'form':form,'plans':plans}
    return render(request,'plan.html',context)

def delete_plan(request,plan_id):
    plan=Plan.objects.get(pk=plan_id)
    plan.delete()
    return redirect('/plan')



def get_status(date_end,date_start):
    now=datetime.date(datetime.now())
    days=timedelta(days=0)
    if (now-date_start>=days) and (date_end-now>=days):
        return (date_end-now).days
    elif (date_end-now<days) and (now-date_start>days):
        return (date_end-now).days
    else :
        return None
def change_bar(request):
    if request.is_ajax and request.method=="GET":
        len_plan=len(Plan.objects.all())
        return JsonResponse({"lenght":len_plan},status=200)
    return JsonResponse({},status=400)
def update_mean(request,*args,**kwargs):
    if request.is_ajax and request.method=="POST":
        model=English.objects.get(word=request.POST['word'])
        model.meaning=request.POST['mean']
        model.example=request.POST['example']
        model.save()
        print(request.POST)
        return JsonResponse({"mean":model.meaning,"example":model.example},status=200)
    return JsonResponse({},status=400)
def show_mean(request):
    if request.is_ajax and request.method=="GET":
        word=request.GET.get("word",None)
        obj=English.objects.get(word=word)
        return JsonResponse({"mean":obj.meaning,"example":obj.example},status=200)
    return JsonResponse({},status=400)


# Create your views here.
