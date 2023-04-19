from django.shortcuts import render

def index(request):
    template = 'base.html'
    return render(request, template)
