from django.shortcuts import render
from django.http import HttpResponseNotFound


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
    if id not in num:
        return HttpResponseNotFound('Такой функции нет')
    context = {'log': logs[id]}
    template = 'logs/system.html'
    return render(request, template, context)
