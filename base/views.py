from django.shortcuts import render
from .models import Group, Message, Comment
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
    messages = Message.objects.all().order_by('-created')
    context = {'groups': groups, 'messages': messages, 'comments': comments}
    return render(request, 'base/home.html', context)

def group(request, pk):
    group = Group.objects.get(id=pk)
    context = {'group': group}
    return render(request, 'base/groups.html', context)

def search_results(request):
    query = request.GET.get('q', '')  # Get the search query from the input field
    return render(request, 'search_results.html', {'query': query})

def login_page(request):
    return render(request, 'login.html')