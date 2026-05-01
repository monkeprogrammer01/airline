from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from flights.models import Booking
from .forms import RegisterForm, ProfileEditForm, AdminUserForm


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=request.user)

    user_bookings = Booking.objects.filter(user=request.user).select_related(
        "flight", "flight__origin", "flight__destination"
    )

    return render(request, 'users/profile.html', {
        'user': request.user,
        "form": form,
        "user_bookings": user_bookings,
    })


@staff_member_required
def admin_users(request):
    users = User.objects.prefetch_related("bookings").all().order_by("username")
    return render(request, "users/admin_users.html", {"users": users})


@staff_member_required
def admin_user_create(request):
    if request.method == "POST":
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get("password")
            if raw_password:
                user.set_password(raw_password)
            else:
                user.set_unusable_password()
            user.save()
            return redirect("admin_users")
    else:
        form = AdminUserForm()
    return render(request, "users/admin_user_form.html", {"form": form, "is_create": True})


@staff_member_required
def admin_user_edit(request, user_id):
    user_obj = User.objects.get(pk=user_id)
    if request.method == "POST":
        form = AdminUserForm(request.POST, instance=user_obj)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get("password")
            if raw_password:
                user.set_password(raw_password)
            user.save()
            return redirect("admin_users")
    else:
        form = AdminUserForm(instance=user_obj)
    return render(request, "users/admin_user_form.html", {"form": form, "is_create": False, "user_obj": user_obj})


@staff_member_required
def admin_user_delete(request, user_id):
    user_obj = User.objects.get(pk=user_id)
    if request.method == "POST":
        user_obj.delete()
        return redirect("admin_users")
    return render(request, "users/admin_user_delete.html", {"user_obj": user_obj})