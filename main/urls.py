from django.template.context_processors import request
from django.urls import path

from .views import *
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', reg_view, name='registration'),
    #path('', TaskList.as_view(), name='tasks'),
    path('', CategoryList.as_view(), name='category-list'),
    path('category-<int:pk>/', category_tasks, name='category_tasks'),
    #path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    #path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('category-<int:category_id>/task-<int:pk>/task-update/', TaskUpdateView.as_view(), name='task-update'),
    path('category-<int:category_id>/task-<int:pk>/delete/', TaskDelete.as_view(), name='task-delete'),
    path('category-<int:category_id>/task-<int:pk>/important-item/', task_important, name='important-item'),
    path('complete-task/<int:pk>/', task_complete, name='task-complete'), #было до в important и update
    path('category-create/', CategoryCreate.as_view(), name='category-create'),
    path('category-<int:category_id>/task-create/', TaskCreate.as_view(), name='task-create'),
]