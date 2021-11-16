from django.shortcuts import render,redirect
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse,JsonResponse
from .models import *
from .form import *
from datetime import datetime,timedelta,date
import random
from django.contrib import messages
from .auto import *
def index(request):
	return render(request,'index.html')
def english(request):
    form=Word_form()
    form_mean=Form_mean()
    if request.method=='POST':
        if 'submit_newword' in request.POST:
            print(request.POST)
            if English.objects.filter(word=request.POST['word']).exists():
                messages.error(request, 'Word already stored!')
                return redirect('/english')
            else:
                form = Word_form(request.POST)
                if form.is_valid():
                    form.save()
                    try:
                        data=auto_mean(request.POST['word'])
                        model=English.objects.get(word=request.POST['word'])
                        model.meaning=data[1]
                        model.example=data[2]
                        model.type=data[0]
                        model.save()
                    except IndexError:
                        pass
                    return redirect('/english') 
    current_week=date.today().isocalendar()[1]
    words=English.objects.filter(pub_date__week=current_week).order_by('-pub_date','-id')
    words_ques=list(English.objects.all())
    lenght=len(words_ques)
    questions=random.sample(words_ques,int(lenght*2/3))
    context={'words':words,'form':form,'form_mean':form_mean,'questions':questions,'lenght':lenght}
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
    for plan in plans :
        plan.status=get_status(plan.date_end,plan.date_start)
        plan.save()
    
    context={'form':form,'plans':plans}
    return render(request,'plan.html',context)

def delete_plan(request,plan_id):
    plan=Plan.objects.get(pk=plan_id)
    plan.delete()
    return redirect('/plan')
def delete_word(request,word_id):
    word=English.objects.get(pk=word_id)
    word.delete()
    return redirect('/english')

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
def update_mean(request):
    if request.is_ajax and request.method=="POST":
        print(request.POST)
        if 'submit_mean' in request.POST:
            model=English.objects.get(word=request.POST['word'])
            model.meaning=request.POST['mean']
            model.example=request.POST['example']
            model.type=request.POST['type']
            model.save()
            return JsonResponse({"mean":model.meaning,"example":model.example,"type":model.type},status=200)
        else:
            return JsonResponse({"error":"not found"},status=400)
    return JsonResponse({"error":"not found"},status=400)
def show_mean(request):
    if request.is_ajax and request.method=="GET":
        word=request.GET.get("word",None)
        obj=English.objects.get(word=word)
        return JsonResponse({"mean":obj.meaning,"example":obj.example,"type":obj.type},status=200)
    return JsonResponse({"error":"not found"},status=400)

def search_word(request):
    if request.is_ajax and request.method=="GET":
        search_word=request.GET.get("search_word",None)
        if English.objects.filter(word=search_word).exists():
            data=English.objects.get(word=search_word)
            return JsonResponse({'mes':'Have word','mean':data.meaning,'example':data.example,'type':data.type,'word':data.word},status=200) 
        else:
            return JsonResponse({},status=400)
    return JsonResponse({},status=400)

# Create your views here.
