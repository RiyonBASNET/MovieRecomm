from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from . forms import LoginForm, UserEditForm
from django.contrib.auth.decorators import login_required
from . auth import admin_only
from app.models import MovieInfo,Genres
from django.core.paginator import Paginator

# Create your views here.

def registerUser(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'User registration successful!')
            return redirect('/login')
        else:
            messages.add_message(request,messages.ERROR,'Error registering. Try again!')
            return render(request,'accounts/register.html', {'form':form})

    context={
        'form':UserCreationForm
    }
    return render(request,'accounts/register.html',context)


def loginUser(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('/dashboard')
                else:
                    return redirect('/')
            else:
                messages.add_message(request,messages.ERROR,'User not found.')
                return render(request,'accounts/login.html',{'form':form})
    context={
        'form':LoginForm
    }
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)

    return redirect('/')

@login_required
@admin_only
def dashboard(request):
    users=User.objects.all().order_by('id')
    movies_count=MovieInfo.objects.count()
    genres_count=Genres.objects.count()

    paginator = Paginator(users,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'page_obj':page_obj,
        'movies_list':movies_count,
        'genres_list':genres_count,
    }

    return render(request,'accounts/dashboard.html',context)

@login_required
@admin_only
def delete_user(request,userId):
    user=get_object_or_404(User,id=userId)

    if user.is_staff:
        messages.error(request,"Unable to remove admin. Please discuss with other admins.")
        return redirect('admin-dashboard')
    else:
        user.delete()
        messages.success(request,"User has been offed ;)")

    return redirect('admin-dashboard')

@login_required
@admin_only
def edit_user(request, userId):
    user = get_object_or_404(User, id=userId)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('admin-dashboard') 
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = UserEditForm(instance=user)
    
    context = {
        'form': form,
        'edit_user': user,
    }
    return render(request, 'accounts/editUserInfo.html', context)