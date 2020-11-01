from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from Users.models import Topic,Alumini,College,Entry,Locations,Salary
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from Users.forms import TopicForm,EntryForm,AluminiSignUpForm,CollegeSignUpForm
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from Users.decorators import alumini_required,college_required
from pygal.style import DarkStyle
import pygal
import pygal_maps_world
from pygal.maps.world import COUNTRIES
from django.db.models import Count

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    return render(request, 'Users/index.html')

@login_required
def topics(request):
    if(request.user.is_alumini==True):
        alumini=Alumini.objects.get(user=request.user)
        topics = Topic.objects.filter(owner=alumini.college).order_by('date_added')
    else:
        college=College.objects.get(user=request.user)
        topics = Topic.objects.filter(owner=college).order_by('date_added')
    

  #topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'Users/topics.html', context)

@login_required
def topic(request, topic_id):
  topic = Topic.objects.get(id=topic_id)
  if(request.user.is_alumini==True):
      alumini=Alumini.objects.get(user=request.user)
      if(topic.owner!=alumini.college):
          raise Http404
  else:
      college=College.objects.get(user=request.user)
      if(topic.owner!=college):
          raise Http404
  entries = topic.entry_set.order_by('-date_added')
  context = {'topic': topic, 'entries': entries}
  return render(request, 'Users/topic.html', context)


@login_required
def new_topic(request):
    if(request.user.is_college==True):
        if request.method!='POST':
        # No date submitted create a blank form
            form =TopicForm()
        else:
        # Post data submitted;process data.
            form=TopicForm(request.POST)
            if form.is_valid():
                new_topic=form.save(commit=False)
                college=College.objects.get(user=request.user)
                new_topic.owner=college
                new_topic.save()
                return HttpResponseRedirect(reverse('Users:topics'))
        context={'form':form}
        return render(request,'Users/new_topic.html',context)
    else:
        raise Http404

@login_required
def delete_topic(request,topic_id):
    if(request.user.is_college==True):
        Topic.objects.get(id=topic_id).entry_set.all().delete()
        Topic.objects.get(id=topic_id).delete()
        return HttpResponseRedirect(reverse('Users:topics'))
    else:
        return Http404

@login_required
def delete_entry(request,entry_id):
    if(request.user.is_college==True):
        entry=Entry.objects.get(id=entry_id)
        topic=entry.topic
        Entry.objects.get(id=entry_id).delete()
        return HttpResponseRedirect(reverse('Users:topic',args=[topic.id]))
    else:
        return Http404        

@login_required
def new_entry(request,topic_id):
    if(request.user.is_college==True):
        topic=Topic.objects.get(id=topic_id)
        if request.method!='POST':
            form=EntryForm()
        else:
            form=EntryForm(data=request.POST)
            if form.is_valid():
                new_entry=form.save(commit=False)
                new_entry.topic=topic
                new_entry.save()
                return HttpResponseRedirect(reverse('Users:topic',args=[topic_id]))

        context={'topic':topic,'form':form}
        return render(request,'Users/new_entry.html',context)
    else:
        raise Http404


@login_required
def edit_entry(request,entry_id):
    if(request.user.is_college==True):
        entry=Entry.objects.get(id=entry_id)
        topic=entry.topic
        if(request.user.is_alumini==True):
            alumini=Alumini.objects.get(user=request.user)
            if(topic.owner!=alumini.college):
                raise Http404
        else:
            college=College.objects.get(user=request.user)
            if(topic.owner!=college):
                raise Http404
        if request.method != 'POST':
        # initial request ; pre-fill form with the current entry.
            form=EntryForm(instance=entry)
        else:
        # Post data submitted : process data
            form=EntryForm(instance=entry,data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('Users:topic',args=[topic.id]))
        context={'entry':entry, 'topic':topic,'form':form }
        return render(request,'Users/edit_entry.html',context)
    else:
        raise Http404

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as {username}")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "Users/login.html",
                    context={"form":form})
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('Users:index'))

def alumini_register(request):
    if request.method !='POST':
        form=AluminiSignUpForm()
    else:
        form=AluminiSignUpForm(data=request.POST)

        if form.is_valid():
            new_user=form.save()
            # log the user in and then redirect to home page.
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            if authenticated_user:
                login(request,authenticated_user)
                return HttpResponseRedirect(reverse('Users:index'))
            else:
                return render(request,'Users/waiting_page.html')
    context={'form':form}
    return render(request,'Users/alumini_register.html',context)

def college_register(request):
    if request.method !='POST':
        form=CollegeSignUpForm()
    else:
        form=CollegeSignUpForm(data=request.POST)

        if form.is_valid():
            new_user=form.save()
            # log the user in and then redirect to home page.
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('Users:index'))
    context={'form':form}
    return render(request,'Users/college_register.html',context)

@login_required
def alumini_list(request):
    if(request.user.is_college):
        college=College.objects.get(user=request.user)
        aluminis=Alumini.objects.filter(college=college).order_by('user_id')
        aluminis_approved=[]
        aluminis_unapproved=[]
        for alumini in aluminis:
            if alumini.user.is_active:
                aluminis_approved.append(alumini)
            else:
                aluminis_unapproved.append(alumini)
        context={'aluminis_approved':aluminis_approved,'aluminis_unapproved':aluminis_unapproved}
        return render(request,'Users/alumini_list.html',context)
    else:
        raise Http404
@login_required
def approve(request,alumini_user_id):
    alumini=Alumini.objects.get(user_id=alumini_user_id)
    alumini.user.is_active=True
    alumini.user.save()
    return HttpResponseRedirect(reverse('Users:alumini_list'))

@login_required
def worldmap(request):
    worldmap=pygal.maps.world.World(fill=True,interpolate='cubic',style=DarkStyle)
    worldmap.title="Alumini Population"
    k=1
    if(request.user.is_alumini==True):
        college=Alumini.objects.get(user=request.user).college
    else:
        college=College.objects.get(user=request.user)
    for country_code in sorted(COUNTRIES.keys()):
        i=Alumini.objects.filter(location=k,college=college).count()
        k=k+1
        worldmap.add('COUNTRIES[country_code]',{str(country_code):i}) 
  
    context={'world_map':worldmap}
    return worldmap.render_django_response()

@login_required
def income_graph(request):
    income_graph=pygal.Bar(fill=True,interpolate='cubic',style=DarkStyle)
    i=1
    values=[]
    salaries=[]
    if(request.user.is_alumini==True):
        college=Alumini.objects.get(user=request.user).college
    else:
        college=College.objects.get(user=request.user)
    while(i<Salary.objects.all().count()+1):
        k=Alumini.objects.filter(salary=i,college=college).count()
        l=Salary.objects.get(id=i).salary
        values.append(k)
        salaries.append(l)
        i=i+1
    income_graph.title='Income distribution'
    income_graph.x_labels=salaries
    income_graph.add('',values)
    return income_graph.render_django_response()







    

