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

    return render(request, 'main/lists.html', {'categories': categories})

def category_tasks(request, pk):
    category = get_object_or_404(Category, id=pk)
    tasks = category.tasks.all()
    return render(request, 'main/task_list.html', {'category': category, 'tasks': tasks})

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'main/lists.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

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
    template_name = 'main/task_form.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        category = Category.objects.get(pk=self.kwargs['category_id'])
        form.instance.category = category  # Привязываем задачу к категории
        form.instance.user = self.request.user  # Привязываем задачу к пользователю
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_success_url(self):
        # Перенаправляем на страницу категории после создания задачи
        return reverse_lazy('category_tasks', kwargs={'pk': self.kwargs['category_id']})

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CategoryCreate, self).form_valid(form)

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'main/task_form.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        # Привязываем задачу к существующей категории
        task = form.save(commit=False)
        task.category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        task.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return context

    def get_success_url(self):
        # Перенаправляем на страницу категории после обновления задачи
        return reverse_lazy('category_tasks', kwargs={'pk': self.kwargs['category_id']})

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'main/task_confirm_delete.html'

    def get_success_url(self):
        # Перенаправление на страницу категории задачи
        return reverse_lazy('category_tasks', kwargs={'pk': self.object.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object.category  # Передаем категорию в шаблон
        return context

def task_important(request, pk):
    item = Task.objects.get(id=pk)
    if not item.important:
        item.important = True
    else:
        item.important = False
    item.save()
    return redirect('category_tasks')

def task_complete(request, pk):
    item = Task.objects.get(id=pk)
    if not item.complete:
        item.complete = True
    else:
        item.complete = False
    item.save()
    return redirect('category_tasks')