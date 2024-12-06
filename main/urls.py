from django.template.context_processors import request
from django.urls import path

from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete, login_view, reg_view, \
    logout_view, task_important, task_complete
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', reg_view, name='registration'),
    path('', TaskList.as_view(), name='tasks'),
    #path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('important-item/<int:pk>/', task_important, name='important-item'),
    path('complete-task/<int:pk>/', task_complete, name='task-complete'),
]