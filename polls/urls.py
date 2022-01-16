from django.urls import path
from . import views

app_name="polls"
urlpatterns=[path('logout/',views.logout,name="logout")
,path('',views.login,name="login")
,path('index/',views.index,name="index")
,path('english/',views.english,name='english')
,path('plan/',views.plan,name='plan')
,path('note/',views.note,name='note')
,path('challenge/',views.challenge,name='challenge')
,path('delete_plan/<plan_id>/',views.delete_plan,name='delete-plan')
,path('change_bar/',views.change_bar,name='change_bar')
,path('update_mean/',views.update_mean,name='update_mean')
,path('show_mean/',views.show_mean,name='show_mean')
,path('delete_word/<word_id>/',views.delete_word,name='delete-word')
,path('search_word',views.search_word,name="search_word")
,path('check_done',views.check_done,name="check_done")
,path('delete_task/<do_id>/',views.delete_task,name='delete_task')
,path('delete_note/<note_id>/',views.delete_note,name='delete_note')
,path('delete_challenge/<challenge_id>/',views.delete_challenge,name='delete_challenge')
,path('update_challenge',views.update_challenge,name="update_challenge")
,
]
