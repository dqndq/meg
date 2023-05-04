from django.shortcuts import render
from django.http import HttpResponseNotFound
from .forms import ReadFile


logs = [
    {
        'funk': 'System',
        'id': 0
    },
    {
        'funk': 'Sysmon',
        'id': 1
    },
    {
        'funk': 'Security',
        'id': 2
    },
]

num = set(log['id'] for log in logs)


def system(request, id):
    template = 'logs/system.html'
    if id not in num:
        return HttpResponseNotFound('Такой функции нет')
    form = ReadFile(request.GET or None)
    if form.is_valid():
        pass
    context = {
        'log': logs[id],
        'form': form
    }
    return render(request, template, context)
