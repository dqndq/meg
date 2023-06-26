from django.shortcuts import render

logs = [
    {
        'funk': 'Linux events',
        'id': 0
    },
]


def index(request):
    context = {'logs': logs}
    template = 'homepage/index.html'
    return render(request, template, context)
