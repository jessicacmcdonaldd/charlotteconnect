from django.shortcuts import render
from .models import Group, Message
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
    messages = Message.objects.all().order_by('-created')
    context = {'groups': groups, 'messages': messages}
    return render(request, 'base/home.html', context)

def group(request, pk):
    group = Group.objects.get(id=pk)
    groups = Group.objects.all()
    context = {'group': group, 'groups': groups}
    return render(request, 'base/groups.html', context)

def search_results(request):
    query = request.GET.get('q', '')
    groups = Group.objects.all()
    return render(request, 'search_results.html', {'query': query})

def login_page(request):
    groups = Group.objects.all()
    return render(request, 'login.html')