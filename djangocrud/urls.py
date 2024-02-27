"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("tasks/", views.tasks, name="tasks"),
    path("signout/", views.signout, name="signout"),
    path("signin/", views.signin, name="signin"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/completed/", views.tasks_completed, name="tasks_completed"),
    path("create/task/", views.create_task, name="create_task"),
    path("detail/task/<int:task_id>/", views.detail_task, name="detail_task"),
    path("complete/task/<int:task_id>/", views.complete_task, name="complete_task"),
    path("delete/task/<int:task_id>/", views.delete_task, name="delete_task"),
]
