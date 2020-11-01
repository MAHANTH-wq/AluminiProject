from django.urls import  path,re_path
from django.conf.urls import url
from .views import classroom
from django.contrib.auth import login

app_name='Users'

urlpatterns=[
    path('',classroom.home,name='index'),
    path('topics/',classroom.topics, name='topics'),
    re_path(r'^topics/(?P<topic_id>\d+)/$',classroom.topic,name='topic'),
    url(r'^new_topic/$', classroom.new_topic, name='new_topic'),
    url(r'^new_entry/(?P<topic_id>\d+)/$',classroom.new_entry,name='new_entry'),
    url(r'^edit_entry/(?P<entry_id>\d+)/$', classroom.edit_entry,name='edit_entry'),
    url(r'^login/$',classroom.login_view,name='login'),
    url(r'^logout/$',classroom.logout_view,name='logout'),
    url(r'^alumini_register/$',classroom.alumini_register,name='alumini_register'),
    url(r'^college_register/$',classroom.college_register,name='college_register'),
    url(r'^alumini_list/$',classroom.alumini_list,name='alumini_list'),
    url(r'^approve/(?P<alumini_user_id>\d+)/$', classroom.approve,name='approve'),
    url(r'^delele_topic/(?P<topic_id>\d+)/$',classroom.delete_topic,name='delete_topic'),
    url(r'^delete_entry/(?P<entry_id>\d+)/$', classroom.delete_entry,name='delete_entry'),
    url(r'^world_map/$',classroom.worldmap,name='world_map'),
    url(r'^income_graph/$',classroom.income_graph,name='income_graph'),
]