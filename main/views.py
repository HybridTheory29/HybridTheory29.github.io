from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context_processors import request
from django.views.generic.list import  ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from main.models import *
from main.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


def login_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        usr = authenticate(request, username=login, password=password)
        if usr is not None:
            user_login(request, usr)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'main/login_form.html')

    return render(request, 'main/login_form.html')

def reg_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            User.objects.create_user(login, password=password)
            usr = authenticate(request, username=login, password=password)
            if usr is not None:
                user_login(request, usr)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'main/login_form.html')

    return render(request, 'main/reg_form.html')

def logout_view(request):
    user_logout(request)
    return HttpResponseRedirect('/login')

def lists(request):
    categories = Category.objects.all()

    context = {
    'categories': categories
    }

    return render(request, 'main/lists.html', context)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

"""
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', "description"]
    success_url = reverse_lazy('tasks')
"""

def taskUpdate(request, pk):
    instance = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MyModelForm(instance=instance)
    return render(request, 'main/task_form.html', {'form': form})


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

def task_important(request, pk):
    item = Task.objects.get(id=pk)
    if not item.important:
        item.important = True
    else:
        item.important = False
    item.save()
    return redirect('tasks')

def task_complete(request, pk):
    item = Task.objects.get(id=pk)
    if not item.complete:
        item.complete = True
    else:
        item.complete = False
    item.save()
    return redirect('tasks')