from django.urls import path
from . import views

app_name="polls"
urlpatterns=[path('',views.index,name="index")
,path('english/',views.english,name='english')
,path('plan/',views.plan,name='plan')
,path('delete_plan/<plan_id>/',views.delete_plan,name='delete-plan')
,path('change_bar/',views.change_bar,name='change_bar')
,path('update_mean/',views.update_mean,name='update_mean')
,path('show_mean/',views.show_mean,name='show_mean')
]
