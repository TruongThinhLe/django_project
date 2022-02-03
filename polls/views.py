from typing import List
from django.shortcuts import render,redirect
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse,JsonResponse
from .models import *
from .form import *
from datetime import datetime,timedelta,date
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login ,logout as dj_logout
from django.contrib.auth.decorators import login_required
from .auto import *
from .algorithm import rate

def logout(request):
    dj_logout(request)
    return redirect("/")

def login(request):
    form=LoginForm(request.POST)
    if form.is_valid():
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user != None:
            dj_login(request,user)
            return redirect("index/")
        else:
            return HttpResponse("Wrong pass or user")
    context={'form':form}
    return render(request,'login.html',context)

@login_required
def index(request):
    current=date.today()
    refresh=List_todo.objects.all()
    for ref in refresh:
        if (ref.Day_todo.isocalendar()[1] != current.isocalendar()[1]):
            ref.delete()
    #=Plan.objects.filter(pub_date__week=current).order_by('-pub_date','-id')
    plans=Plan.objects.all()
    for plan in plans:
        if (plan.date_end>=current) and (plan.date_start<=current) and ((plan.date_start-current).days%plan.period_day==0):
            if(List_todo.objects.filter(Task_todo=plan.plan,Day_todo=current).exists()) :
                #todo_s=List_todo.objects.get(Task_todo=plan.plan)
                #todo_s.Day_todo=current
                #todo_s.save()
                pass
            else :
                todo_s=List_todo(Task_todo=plan.plan,Day_todo=current,Time_todo=plan.time_todo)
                todo_s.save()
    form=Todo_form()
    if request.method=='POST':
        if Todo_form(request.POST).is_valid():
            post=request.POST.copy()
            print(post)
            if post["daydo"]:
                post.pop("csrfmiddlewaretoken")
                if post["daydo"]=="Today":
                    post["Day_todo"]=str(current)
                    post.pop("daydo")
                    List_todo.objects.create(**post.dict())
                    return redirect("/index")
                else:
                    post["Day_todo"]=str(current+timedelta(days=1))
                    post.pop("daydo")
                    List_todo.objects.create(**post.dict())
                    return redirect("/index")

    todo_today=List_todo.objects.filter(Day_todo=current)
    count_today=0
    for do in todo_today:
        count_today=count_today+do.Time_todo
    todo_tommorrow=List_todo.objects.filter(Day_todo=current+timedelta(days=1))
    count_tommor=0
    for do in todo_tommorrow:
        count_tommor=count_tommor+do.Time_todo

    monday=current-timedelta(days=current.isoweekday()-1)
    list_day=[monday+timedelta(days=x) for x in range(0,7)]        
    re_task=[]
    for day in list_day:
        tas=Sub_do(day)
        re_task.append(tas)
    print(re_task)
    #xu ly cho status update
    note_all=list(Note.objects.filter(Time_pub__lt=current))
    review_note=[]
    for no in note_all:
        if ((no.Time_pub-current).days%3==0):
            review_note.append(no)
    note=Note.objects.filter(Time_pub=current)
    challenge=Challenge.objects.filter(Status=False)
    plan=Plan.objects.all()
    st_plan=0
    for pl in plan:
        if rate(pl.date_end,pl.date_start)>60:
            st_plan+=1

    status={'st_note':len(note),'st_challenge':len(challenge),'st_plan':st_plan}

    context={'todo':todo_today,'form':form,'tomr_do':todo_tommorrow,'count_today':count_today,'count_tommor':count_tommor,'re_task':re_task,'status':status,'review_note':review_note}
    return render(request,'index.html',context)

@login_required
def english(request):
    form=Word_form()
    form_mean=Form_mean()
    form_num=Num_form()
    number_quiz=10
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
        elif 'OK' in request.POST:
            number_quiz=int(request.POST['number_quiz'])
    current=date.today().isocalendar()[1]
    words=English.objects.filter(pub_date__week=current).order_by('-pub_date','-id')
    words_ques=list(English.objects.all())
    lenght=len(words_ques)
    if lenght>number_quiz :
        questions=random.sample(words_ques,number_quiz)
        for i in range(0,len(questions)):
            if questions[i].example==None:
                continue
            else:
                questions[i].example=questions[i].example.replace(questions[i].word,"___")
    else :
        questions=random.sample(words_ques,int(lenght))
        for i in range(0,len(questions)):
            if questions[i].example==None:
                continue
            else:
                questions[i].example=questions[i].example.replace(questions[i].word,"___")
    questions_ques=random.sample(questions,len(questions))
    context={'words':words,'form':form,'form_mean':form_mean,'questions':questions,'questions_ques':questions_ques,'lenght':lenght,'form_num':form_num,'number_quiz':number_quiz}
    return render(request,'english.html',context)

@login_required
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

@login_required
def note(request):
    form=Note_Form()
    if request.method=='POST':
        print(request.POST)
        form=Note_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/note')
    note_data=Note.objects.all().order_by('-Time_pub','-id')
    context={"form":form,"note_data":note_data}
    return render(request,'note.html',context)

@login_required
def challenge(request):
    form=Challenge_form()
    if request.method=='POST':
        form=Challenge_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/challenge')
    challenge=Challenge.objects.all().order_by('-Time_pub','-id')
    context={"form":form,'challenge':challenge}
    return render(request,'challenge.html',context)

@login_required
def delete_plan(request,plan_id):
    plan=Plan.objects.get(pk=plan_id)
    plan.delete()
    return redirect('/plan')

@login_required
def delete_word(request,word_id):
    word=English.objects.get(pk=word_id)
    word.delete()
    return redirect('/english')

@login_required
def delete_note(request,note_id):
    note=Note.objects.get(pk=note_id)
    note.delete()
    return redirect('/note')

@login_required
def delete_challenge(request,challenge_id):
    challenge=Challenge.objects.get(pk=challenge_id)
    challenge.delete()
    return redirect('/challenge')

def get_status(date_end,date_start):
    now=datetime.date(datetime.now())
    days=timedelta(days=0)
    if (now-date_start>=days) and (date_end-now>=days):
        return (date_end-now).days
    elif (date_end-now<days) and (now-date_start>days):
        return (date_end-now).days
    else :
        return None

@login_required
def change_bar(request):
    if request.is_ajax and request.method=="GET":
        len_plan=len(Plan.objects.all())
        return JsonResponse({"lenght":len_plan},status=200)
    return JsonResponse({},status=400)

@login_required
def update_mean(request):
    if request.is_ajax and request.method=="POST":
        print(request.POST)
        if 'submit_mean' in request.POST:
            model=English.objects.get(word=request.POST['word'])
            model.meaning=request.POST['mean']
            model.example=request.POST['example']
            model.type=request.POST['type']
            model.save()
            return JsonResponse({"mean":model.meaning,"example":model.example,"type":model.type,"id":model.id},status=200)
        else:
            return JsonResponse({"error":"not found"},status=400)
    return JsonResponse({"error":"not found"},status=400)

@login_required
def show_mean(request):
    if request.is_ajax and request.method=="GET":
        word=request.GET.get("word",None)
        obj=English.objects.get(word=word)
        return JsonResponse({"mean":obj.meaning,"example":obj.example,"type":obj.type,'id':obj.id},status=200)
    return JsonResponse({"error":"not found"},status=400)

@login_required
def search_word(request):
    if request.is_ajax and request.method=="GET":
        search_word=request.GET.get("search_word",None)
        if English.objects.filter(word=search_word).exists():
            data=English.objects.get(word=search_word)
            return JsonResponse({'mes':'Have word','mean':data.meaning,'example':data.example,'type':data.type,'word':data.word,'id':data.id},status=200) 
        else:
            return JsonResponse({},status=400)
    return JsonResponse({},status=400)

@login_required
def check_done(request):
    current=date.today()
    if request.method=="GET":
        task=request.GET.copy()
        print(list(task.keys()))
        listdo=List_todo.objects.filter(Day_todo=current)
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
    return redirect('/index')

@login_required
def update_challenge(request):
    if request.method=="GET":
        challenge=request.GET.copy()
        lis_chag=Challenge.objects.all()
        for lis in lis_chag:
            for cha in list(challenge.keys()):
                if lis.Challenge==cha:
                    lis.Status=True
                    lis.save()
                    break
                else:
                    lis.Status=False
                    lis.save()
    return redirect('/challenge')

@login_required
def delete_task(request,do_id):
    task=List_todo.objects.get(pk=do_id)
    task.delete()
    return redirect('/index')

@login_required
def review_task(request):
    if request.method=='GET':
        data=request.GET.get('id')
        data_req=Note.objects.get(pk=data)
        return JsonResponse({'data':data_req.Detail},status=200)
    return JsonResponse({},status=400)

# Create your views here.
