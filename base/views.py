from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, Message, Comment, Profile
from .forms import ProfileForm, MessageForm, CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    # comments = Comment.objects.filter(message_in=messages).order_by('created')
    groups = Group.objects.all()
    user_courses = get_user_courses(request.user)

    context = {'group': group, 'messages': messages,'groups': groups, 'user_courses':user_courses,}
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
        return redirect('profile') 

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

# Login required for user to create a post
def create_post(request, group_id=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            if group_id:
                message.group = Group.objects.get(id=group_id)
            message.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

# View posts

def post_view(request, post_id):
    groups = Group.objects.all()
    message = get_object_or_404(Message, pk=post_id)
    comments = Comment.objects.filter(message=message)
    user_courses = get_user_courses(request.user)

    context = {
        'message': message,
        'comments': comments,
        'groups': groups,
        'user_courses':user_courses,
    }

    return render(request, 'post_view.html', context)

@csrf_exempt
@login_required
def post_comment(request, post_id):
    if request.method == "POST":
        message = get_object_or_404(Message, pk=post_id)
        body = request.POST.get("comment_body", "").strip()
        if body:
            Comment.objects.create(
                message=message,
                author=request.user,
                group=message.group,
                body=body
            )
            return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

def register_page(request):
    if request.user.is_authenticated:
        return redirect('profile')

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()

            profile = Profile.objects.create(user=user)
            enrolled_courses = form.cleaned_data.get('enrolled_courses')
            profile.enrolled_courses.set(enrolled_courses)

            login(request, user)
            return redirect('profile')

    groups = Group.objects.all()
    return render(request, 'base/register.html', {'form': form, 'groups': groups})