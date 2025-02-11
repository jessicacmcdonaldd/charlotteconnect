from django.shortcuts import render
from .models import Group
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
    context = {'groups': groups}
    return render(request, 'base/home.html', context)

def group(request, pk):
    group = Group.objects.get(id=pk)
    context = {'group': group}
    return render(request, 'base/groups.html', context)