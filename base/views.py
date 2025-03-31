from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, Message, Comment, Profile
from .forms import ProfileForm

# groups = [
#     {'id':1, 'name':'ITSC 4155 Spring 2025'},
#     {'id':2, 'name':'ITCS 3156 Spring 2025'},
#     {'id':3, 'name':'ECON 2101 Spring 2025'},
# ]

def home(request):
#     groups = [
#     {'id':1, 'name':'ITSC 4155 Spring 2025'},
#     {'id':2, 'name':'ITCS 3156 Spring 2025'},
#     {'id':3, 'name':'ECON 2101 Spring 2025'},
# ]
    groups = Group.objects.all()
    comments = Comment.objects.all()
    messages = Message.objects.filter(group__isnull=True).order_by('-created')
    context = {'groups': groups, 'messages': messages, 'comments': comments}
    return render(request, 'base/home.html', context)

def group(request, pk):
    group = Group.objects.get(id=pk)
    messages = Message.objects.filter(group=group).order_by('-created')
    groups = Group.objects.all()
    context = {'group': group, 'messages': messages, 'groups': groups}
    return render(request, 'base/groups.html', context)

def search_results(request):
    query = request.GET.get('q', '')
    groups = Group.objects.all()
    return render(request, 'search_results.html', {'query': query})

def login_page(request):
    groups = Group.objects.all()
    return render(request, 'base/login.html')

@login_required(login_url='login')
def profile_page(request):
    groups = Group.objects.all()
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'base/profile.html', {'profile': profile, 'form': form})