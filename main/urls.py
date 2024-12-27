from django.template.context_processors import request
from django.urls import path

from .views import *
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', reg_view, name='registration'),
    path('', TaskList.as_view(), name='tasks'),
    path('lists/', lists, name='lists'),
    path('category/<int:category_id>/', category_tasks, name='category_tasks'),
    #path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', taskUpdate, name='task-update'), #TaskUpdate.as_view()
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('important-item/<int:pk>/', task_important, name='important-item'),
    path('complete-task/<int:pk>/', task_complete, name='task-complete'),
    path('category-create/', CategoryCreate.as_view(), name='category-create')
]