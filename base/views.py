from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, Message, Comment, Profile
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.db.models import Q

# groups = [
#     {'id':1, 'name':'ITSC 4155 Spring 2025'},
#     {'id':2, 'name':'ITCS 3156 Spring 2025'},
#     {'id':3, 'name':'ECON 2101 Spring 2025'},
# ]
def get_user_courses(user):
    if user.is_authenticated:
        try:
            profile = Profile.objects.get(user=user)
            return profile.enrolled_courses.all()
        except Profile.DoesNotExist:
            return []
    return []

def home(request):
#     groups = [
#     {'id':1, 'name':'ITSC 4155 Spring 2025'},
#     {'id':2, 'name':'ITCS 3156 Spring 2025'},
#     {'id':3, 'name':'ECON 2101 Spring 2025'},
# ]

# Home Page / Search Functionality

    query = request.GET.get("q")
    groups = Group.objects.all()
    comments = Comment.objects.all()
    user_courses = get_user_courses(request.user)

    if query:
        messages_query = Message.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).order_by("-created")
    else:
        messages_query = Message.objects.filter(group__isnull=True).order_by("-created")

    context = {
            'groups': groups, 
            'messages': messages_query, 
            'comments': comments, 
            'user_courses':user_courses,
        }

    return render(request, 'base/home.html', context)

#Groups

def group(request, pk):
    group = Group.objects.get(id=pk)
    messages = Message.objects.filter(group=group).order_by('-created')
    groups = Group.objects.all()
    user_courses = get_user_courses(request.user)
    context = {'group': group, 'messages': messages, 'groups': groups, 'user_courses':user_courses,}
    return render(request, 'base/groups.html', context)

#Search Reults

def search_results(request):
    query = request.GET.get('q', '')
    if query:
        results = Message.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    else:
        results = Message.objects.none()
    
    return render(request, "search_results.html", {'results':results, "query":query})

# Login Page

def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Incorrect username or password. Please try again.')

    groups = Group.objects.all()
    return render(request, 'base/login.html', {'groups': groups})

# Login Authentication

@login_required(login_url='login')
def profile_page(request):
    groups = Group.objects.all()
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile)
    user_courses = get_user_courses(request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'base/profile.html', {'profile': profile, 'form': form, 'groups': groups, 'user_courses':user_courses,})

def logout_view(request):
    logout(request)
    return redirect('login')