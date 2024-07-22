from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, 'home.html')


def find(request):
    return render(request, 'find.html')


def supplies(request):
    return render(request, 'supplies.html')


def agrovet(request):
    return render(request, 'agrovet.html')


def community(request):
    return render(request, 'community.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')