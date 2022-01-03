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
    current=date.today()
    refresh=List_todo.objects.all()
    for ref in refresh:
        if (ref.Day_todo.isocalendar()[1] != current.isocalendar()[1]):
            ref.delete()
    #=Plan.objects.filter(pub_date__week=current).order_by('-pub_date','-id')
    plans=Plan.objects.all()
    for plan in plans:
        if (plan.date_end>=current) and (plan.date_start<current):
            if(List_todo.objects.filter(Task_todo=plan.plan).exists()):
                todo_s=List_todo.objects.filter(Task_todo=plan.plan)
                todo_s.Day_todo=current
            else :
                todo_s=List_todo(Task_todo=plan.plan,Day_todo=current)
                todo_s.save()
    form=Todo_form()
    if request.method=='POST':
        if Todo_form(request.POST).is_valid():
            post=request.POST.copy()
            print(post)
            if post["Today"]:
                post["Day_todo"]=str(current)
                post.pop("csrfmiddlewaretoken")
                post.pop("Today")
                List_todo.objects.create(**post.dict())
                return redirect("/")
            else:
                post["Day_todo"]=str(current+timedelta(days=1))
                post.pop("csrfmiddlewaretoken")
                post.pop("Tommoror")
                List_todo.objects.create(**post.dict())
                return redirect("/")

    todo_today=List_todo.objects.filter(Day_todo=current)
    todo_tommorrow=List_todo.objects.filter(Day_todo=current+timedelta(days=1))
    context={'todo':todo_today,'form':form,'tomr_do':todo_tommorrow}
    return render(request,'index.html',context)

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
    current=date.today().isocalendar()[1]
    words=English.objects.filter(pub_date__week=current).order_by('-pub_date','-id')
    words_ques=list(English.objects.all())
    lenght=len(words_ques)
    if lenght>20 :
        questions=random.sample(words_ques,20)
        for i in range(0,len(questions)):
            questions[i].example=questions[i].example.replace(questions[i].word,"___")
    else :
        questions=random.sample(words_ques,int(lenght))
        for i in range(0,len(questions)):
            questions[i].example=questions[i].example.replace(questions[i].word,"___")
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
def check_done(request):
    if request.method=="GET":
        task=request.GET.copy()
        print(list(task.keys()))
        listdo=List_todo.objects.all()
        for lis in listdo:
            for tas in list(task.keys()):
                print(tas)
                print(lis.Task_todo+'.')
                if lis.Task_todo==tas:
                    lis.Check_done=True
                    lis.save()
                    break
                else:
                    lis.Check_done=False
                    lis.save()
        
    return redirect('/')
# Create your views here.
