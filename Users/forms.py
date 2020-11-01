from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from Users.models import ( User,Alumini,College,Topic,Entry,Locations,Salary)


class CollegeSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_college = True
        user.save()
        college=College.objects.create(user=user)
        college.save()
        return user


class AluminiSignUpForm(UserCreationForm):
    colleges = forms.ModelChoiceField(queryset=College.objects.all(),required=True)
    locations=forms.ModelChoiceField(queryset=Locations.objects.all(),required=True)
    salary=forms.ModelChoiceField(queryset=Salary.objects.all(),required=True)
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_alumini= True
        user.is_active=False
        user.save()
        alumini = Alumini(user=user,college=self.cleaned_data['colleges'],location=self.cleaned_data['locations'],
        salary=self.cleaned_data['salary'])
        alumini.save()
        return user

class TopicForm(forms.ModelForm):
    class Meta:
        model=Topic
        fields=['text']
        labels={'text':'write here'}
class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['text']
        labels={'text':''}
        widgets={'text':forms.Textarea(attrs={'cols':80})}


