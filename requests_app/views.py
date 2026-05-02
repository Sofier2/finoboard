from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
        budget = request.POST.get('budget')  # optional

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


# 🔹 СПИСОК ВСІХ ЗАЯВОК
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
    requests = Request.objects.filter(
        author=request.user
    ).order_by('-id')

    return render(request, 'my_requests.html', {
        'requests': requests
    })


# 🔹 ВИДАЛЕННЯ ЗАЯВКИ
@login_required
def delete_request(request, id):
    req = get_object_or_404(Request, id=id)

    # 🔒 тільки автор може видалити
    if req.author == request.user:
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# 🔹 ЛОГАУТ
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')