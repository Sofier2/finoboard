from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Request, Vote


# 🔹 ГОЛОВНА
def home(request):
    return render(request, 'home.html')


# 🔹 СТВОРЕННЯ ЗАЯВКИ
@login_required
def create_request(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        budget = request.POST.get('budget')

        if title and description:
            Request.objects.create(
                title=title,
                description=description,
                votes=0,
                author=request.user,
                budget=budget if budget else None
            )

        return redirect('list')

    return render(request, 'create_request.html')


# 🔹 СПИСОК ЗАЯВОК
def list_requests(request):
    sort = request.GET.get('sort')

    if sort == 'new':
        requests = Request.objects.all().order_by('-id')
    else:
        requests = Request.objects.all().order_by('-votes')

    return render(request, 'list_requests.html', {
        'requests': requests
    })


# 🔹 ГОЛОСУВАННЯ
@login_required
def vote(request, request_id):
    req = get_object_or_404(Request, id=request_id)

    vote, created = Vote.objects.get_or_create(
        user=request.user,
        request=req
    )

    if created:
        req.votes += 1
        req.save()

    return redirect('list')


# 🔹 МОЇ ЗАЯВКИ
@login_required
def my_requests(request):
    requests = Request.objects.filter(author=request.user).order_by('-id')

    return render(request, 'my_requests.html', {
        'requests': requests
    })


# 🔹 ВИДАЛЕННЯ
@login_required
def delete_request(request, id):
    req = get_object_or_404(Request, id=id)

    if req.author == request.user or request.user.is_superuser:
        req.delete()

    return redirect('my_requests')


# 🔹 РЕЄСТРАЦІЯ
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                login(request, user)
                return redirect('home')

    return render(request, 'register.html')


# 🔹 ЛОГІН
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.is_staff:
                return redirect('supervisor_dashboard')
            else:
                return redirect('home')

    return render(request, 'login.html', {'form': form})


# 🔹 ЛОГАУТ
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# 🔴 АДМІН ПАНЕЛЬ (ГОЛОВНЕ ВИПРАВЛЕННЯ)
@login_required
def admin_dashboard(request):
    if not user_is_admin(request.user):
        return redirect('home')

    requests = Request.objects.all().order_by('-id')

    return render(request, 'admin_dashboard.html', {
        'requests': requests
    })


# 🟡 СУПЕРВАЙЗЕР
@login_required
def supervisor_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    return render(request, 'supervisor.html')


# 🔐 перевірка адміна
def user_is_admin(user):
    return user.is_superuser


@login_required
def edit_request(request, id):
    req = get_object_or_404(Request, id=id)

    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        req.title = request.POST.get('title')
        req.description = request.POST.get('description')
        req.budget = request.POST.get('budget')

        req.save()
        return redirect('admin_dashboard')

    return render(request, 'edit_request.html', {
        'req': req
    })