from django.shortcuts import render, redirect
from .models import Group, Message, Comment, SignUpForm
from django.contrib import messages

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
    return render(request, 'login.html')

def registration_page(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')  # You can change this to your desired route
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})
