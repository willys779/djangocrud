from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {
            "form": UserCreationForm
        })
    elif request.method == "POST":
        usuario = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            try:
                user = User.objects.create_user(username= usuario, password= password1)
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError as ex:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "El usuario ya existe."
                })
        
        return render(request, "signup.html", {
            "form": UserCreationForm,
            "error": "Las contraseñas no coinciden."
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user = request.user, dateCompleted__isnull = True)
    return render(request, "tasks.html", {
        "tasks": tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user = request.user, dateCompleted__isnull = False).order_by("-dateCompleted")
    return render(request, "tasks.html", {
        "tasks": tasks
    })

@login_required
def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm
        })
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm,
                "error": "Credenciales incorrectas"
            })
        else:
            login(request, user)
            return redirect("tasks")
        
@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {
            "form": TaskForm
        })
    elif request.method == "POST":
        try:
            form = TaskForm(request.POST)
            newTask = form.save(commit = False)
            newTask.user = request.user
            newTask.save()
            return redirect("tasks")
        except:
            return render(request, "create_task.html", {
            "form": TaskForm,
            "error": "Por favor ingrese datos válidos"
        })

@login_required
def detail_task(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk = task_id, user = request.user)
        form = TaskForm(instance = task)
        return render(request, "task_detail.html", {
            "task": task,
            "form": form
        })
    elif request.method == "POST":
        try:
            task = get_object_or_404(Task, pk = task_id)
            form = TaskForm(request.POST, instance = task)
            form.save()
            return redirect("tasks")
        except:
            return render(request, "task_detail.html", {
            "task": task,
            "form": form,
            "error": "Error actualizando"
        })            

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == "POST":
        task.dateCompleted = timezone.now()
        task.save()
        return redirect("tasks")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")
    
