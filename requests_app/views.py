from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse

from .models import Request, Vote
import citizen_system.arduino_bridge as bridge

# ----------------------------
# 🚫 ADMIN SOFT DELETE
# ----------------------------
@login_required
def admin_delete_request(request, id):

    if not request.user.is_superuser:
        return redirect('home')

    req = get_object_or_404(Request, id=id)

    req.is_deleted = True
    req.deleted_by_admin = True
    req.save()

    return redirect('admin_dashboard')
# ----------------------------
# 🔐 HARDWARE LOGIN PAGE
# ----------------------------
def hardware_login(request):

    user = bridge.authorized_user

    if user is not None:

        login(request, user)

        # очистка після успішного login
        bridge.authorized_user = None
        bridge.authorized_flag = False

        # 👉 одразу кидаємо в правильний кабінет
        if user.is_superuser:
            return redirect('admin_dashboard')
        elif user.is_staff:
            return redirect('supervisor_dashboard')
        else:
            return redirect('home')

    return render(request, 'hardware_wait.html')

# ----------------------------
# 🔐 AJAX CHECK AUTH (ONLY CHECK, NO LOGIN!)
# ----------------------------
def check_hardware_auth(request):

    if bridge.authorized_flag and bridge.authorized_user:

        user = bridge.authorized_user

        return JsonResponse({
            "authenticated": True,
            "username": user.username,
            "redirect": "/hardware-login/"
        })

    return JsonResponse({"authenticated": False})


# ----------------------------
# 🏠 HOME
# ----------------------------
def home(request):
    return render(request, 'home.html')


# ----------------------------
# ➕ CREATE REQUEST
# ----------------------------
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


# ----------------------------
# 📋 LIST REQUESTS
# ----------------------------
def list_requests(request):

    sort = request.GET.get('sort')

    if sort == 'new':
        requests = Request.objects.filter(
            is_deleted=False
        ).order_by('-id')

    elif sort == 'old':
        requests = Request.objects.filter(
            is_deleted=False
        ).order_by('id')

    else:
        requests = Request.objects.filter(
            is_deleted=False
        ).order_by('-votes')

    voted_requests = []

    if request.user.is_authenticated:

        voted_requests = Vote.objects.filter(
            user=request.user
        ).values_list('request_id', flat=True)

    return render(request, 'list_requests.html', {
        'requests': requests,
        'sort': sort,
        'voted_requests': voted_requests
    })

# ----------------------------
# 👍 VOTE
# ----------------------------
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

@login_required
def admin_delete_request(request, id):

    if not request.user.is_superuser:
        return redirect('home')

    req = get_object_or_404(Request, id=id)

    req.is_deleted = True
    req.deleted_by_admin = True

    req.save()

    return redirect('admin_dashboard')

@login_required
def restore_request(request, id):

    if not request.user.is_superuser:
        return redirect('home')

    req = get_object_or_404(Request, id=id)

    req.is_deleted = False
    req.deleted_by_admin = False
    req.save()

    return redirect('admin_dashboard')
# ----------------------------
# 👤 MY REQUESTS
# ----------------------------
@login_required
def my_requests(request):

    requests = Request.objects.filter(
        author=request.user
    ).order_by('-id')

    return render(request, 'my_requests.html', {
        'requests': requests
    })


# ----------------------------
# 🗑 SOFT DELETE
# ----------------------------
@login_required
def delete_request(request, id):

    req = get_object_or_404(Request, id=id)

    if req.author == request.user:

        req.is_deleted = True
        req.deleted_by_admin = False
        req.save()

    return redirect('my_requests')
# ----------------------------
# 🧨 HARD DELETE (FIXED + ADDED)
# ----------------------------
@login_required
def hard_delete_request(request, id):

    if not request.user.is_superuser:
        return redirect('home')

    req = get_object_or_404(Request, id=id)

    req.delete()

    return redirect('admin_dashboard')


# ----------------------------
# 📝 REGISTER
# ----------------------------
def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # перевірка паролів
        if password1 != password2:
            return render(request, 'register.html', {
                'error': 'Паролі не співпадають'
            })

        # перевірка username
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Користувач вже існує'
            })

        # створення користувача
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)

        return redirect('home')

    return render(request, 'register.html')

# ----------------------------
# 🔑 LOGIN
# ----------------------------
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

    return render(request, 'login.html', {
        'form': form
    })


# ----------------------------
# 🚪 LOGOUT
# ----------------------------
@login_required
def logout_view(request):

    logout(request)
    return redirect('home')


# ----------------------------
# 🛡 ADMIN DASHBOARD
# ----------------------------
@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('home')

    requests = Request.objects.all().order_by('-id')

    return render(request, 'admin_dashboard.html', {
        'requests': requests
    })


# ----------------------------
# 🧑‍💼 SUPERVISOR DASHBOARD
# ----------------------------
@login_required
def supervisor_dashboard(request):

    if not request.user.is_staff:
        return redirect('home')

    return render(request, 'supervisor.html')


# ----------------------------
# ✏️ EDIT REQUEST
# ----------------------------
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