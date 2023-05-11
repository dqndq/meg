from django.shortcuts import render
from django.http import HttpResponseNotFound
from .forms import ReadFileForm


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

    if request.method == 'POST':
        form = ReadFileForm(
            request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            form.save()
    else:
        form = ReadFileForm()

    context = {
        'log': logs[id],
        'form': form
    }
    return render(request, template, context)
