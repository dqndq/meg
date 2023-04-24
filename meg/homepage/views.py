from django.shortcuts import render

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


def index(request):
    context = {'logs': logs}
    template = 'homepage/index.html'
    return render(request, template, context)
