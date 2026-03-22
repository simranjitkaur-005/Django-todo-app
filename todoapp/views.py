from django.shortcuts import render, redirect, get_object_or_404
from todoapp.models import Person, Task
from django.contrib import messages


# Register
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        number = request.POST.get("number")

        if not name or not email or not password or not number:
            messages.error(request, "All fields are required")
            return redirect('register')

        if Person.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('login')

        Person.objects.create(
            name=name,
            email=email,
            password=password,
            number=number
        )
        return redirect('login')

    return render(request, 'register.html')


# Login
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Person.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id
            request.session['name'] = user.name
            request.session['is_admin'] = user.is_admin

            if user.is_admin:
                return redirect('showdata')
            return redirect('todoapp')

        messages.error(request, "Invalid credentials")
        return redirect('login')

    return render(request, 'login.html')


# Dashboard
def todoapp(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    person = get_object_or_404(Person, id=user_id)
    tasks = person.tasks.all()

    return render(request, 'todoapp.html', {"tasks": tasks})


# Admin View
def showdata(request):
    if not request.session.get('is_admin'):
        messages.error(request, "Only admin can access this page")
        return redirect('todoapp')

    users = Person.objects.all()
    tasks = Task.objects.all()

    return render(request, 'showdata.html', {
        'dataone': users,
        'datatwo': tasks
    })


# Add Task
def todotask(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    person = get_object_or_404(Person, id=user_id)

    if request.method == "POST":
        task_text = request.POST.get("task")

        if task_text:
            Task.objects.create(person=person, task=task_text)

    return redirect('todoapp')


# ✅ Delete Task
def delete_task(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    task = get_object_or_404(Task, id=id, person_id=user_id)
    task.delete()

    return redirect('todoapp')


# ✅ Edit Task
def edit_task(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    task = get_object_or_404(Task, id=id, person_id=user_id)

    if request.method == "POST":
        new_task = request.POST.get("task")

        if new_task:
            task.task = new_task
            task.save()
            return redirect('todoapp')

    return render(request, 'edit_task.html', {"task": task})


# Logout
def logout(request):
    request.session.flush()
    return redirect('login')