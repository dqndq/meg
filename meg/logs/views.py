from django.shortcuts import render
from django.http import HttpResponseNotFound
from .forms import ReadFileForm
from django.conf import settings
import os
from datetime import datetime
import io
import re


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


def process_file(file):
    ruleREG = r"key=\"[a-z]{0,10}_?[a-z]{0,10}_?[a-z]{0,10}_?[a-z]{0,10}\""
    hostnameREG = r"[ ][a-zA-Z]{0,13}_?-?.?[a-zA-Z]{0,13}_?-?.?[a-zA-Z]{0,13}_?-?.?[a-zA-Z]{0,13}_?-?.? audispd"
    exeREG = r"exe=\".*\" key"
    uidREG = r" uid=[0-9][0-9]?[0-9]?[0-9]?"
    UIDREG = r" UID=\".*\" GID="
    typeREG = r"type=[a-zA-Z]{0,9} msg"
    msg_auditREG = r"msg=audit\([0-9]{0,11}."
    filename = os.path.join(settings.MEDIA_ROOT, file.name)
    with open(filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    results = {}

    def audithost(filename):
        with io.open(filename, encoding='utf-8') as c:
            log = c.read()
            search_auditdhostnames = re.findall(hostnameREG, log)
            filter_hostnames = (re.sub(' audispd', '', str(search_auditdhostnames)))
            ar = (filter_hostnames).replace("['", "").replace("']", "").replace("'", "").split(",")
            print("hostnames from log:", end=' ')
            for el in ar:
                el = str(el)
                print(el)
            results['audithost'] = ar

    def auditexec(filename):
        with io.open(filename, encoding='utf-8') as b:
            log = b.read()
            search_auditdexecs = re.findall(exeREG, log)
            filter_execs = re.sub('exe=', '', str(search_auditdexecs))
            filter_execs2 = re.sub('key', '', str(filter_execs))
            ar = (filter_execs2).replace("['", "").replace("']", "").replace("'", "").split(",")
            print("log process:", end=' ')
            for el in ar:
                el = str(el)
                print(el)
            results['auditexec'] = ar

    def auditdrule(filename):
        with io.open(filename, encoding='utf-8') as d:
            log = d.read()
            search_auditdrules = re.findall(ruleREG, log)
            filter_rule = re.sub('key=', '', str(search_auditdrules))
            ar = (filter_rule).replace("['", "").replace("']", "").replace("'", "").split(",")
            print("auditd rule:", end=' ')
            for el in ar:
                el = str(el)
                print(el)
            results['auditdrule'] = ar

    def auditduid(filename):
        with io.open(filename, encoding='utf-8') as d:
            log = d.read()
            search_auditduids = re.findall(uidREG, log)
            filter_uids = re.sub(' uid=', '', str(search_auditduids))
            ar = (filter_uids).replace("['", "").replace("']", "").replace("'", "").split(",")
            print("log uids(0 for 'root'):", end=' ')
            for el in ar:
                el = str(el)
                print(el)
            results['auditUIDS'] = ar
            

    def auditUIDS(filename):
        with io.open(filename, encoding='utf-8') as b:
            log = b.read()
            search_auditdUIDS = re.findall(UIDREG, log)
            filter_UIDS = re.sub(' UID=', '', str(search_auditdUIDS))
            filter_UIDS2 = re.sub('GID=', '', str(filter_UIDS))
            ar = (filter_UIDS2).replace("['", "").replace("']", "").replace("'", "").split(",")
            print("log username:", end=' ')
            for el in ar:
                el = str(el)
                print(el)
            results['auditUIDS'] = ar

    def audittype(filename):
        with io.open(filename, encoding='utf-8') as b:
            log = b.read()
            search_auditdtype = re.findall(typeREG, log)
            filter_type = re.sub('type=', '', str(search_auditdtype))
            filter_type2 = re.sub(' msg', '', str(filter_type))
            ar = (filter_type2).replace("['", "").replace("']", "").replace("'", "").split(",")
            print("audit type:", end=' ')
            for el in ar:
                print(el)
            results['audittype'] = ar

    def auditmsg_audit(filename):
        with io.open(filename, encoding='utf-8') as b:
            log = b.read()
            search_auditdmsg = re.findall(msg_auditREG, log)
            filter_msg = re.sub("msg=audit\(", '', str(search_auditdmsg))
            filter_msg2 = re.sub("\.", '', str(filter_msg))
            ar = (filter_msg2).replace("['","").replace("']","").replace("'","").split(",")
            print('log timestamp:', end=' ')
            le = []
            for el in ar:
                el = int(el)
                x = (datetime.utcfromtimestamp(el).strftime('%d-%m-%Y %H:%M:%S'))
                le.append(x)
            results['auditmsg_audit'] = le

    auditdrule(filename)
    audithost(filename)
    auditexec(filename)
    auditduid(filename)
    auditUIDS(filename)
    audittype(filename)
    auditmsg_audit(filename)
    return results

def parse_file(request):
    template = 'logs/system.html'
    if request.method == 'POST':
        form = ReadFileForm(
            request.POST,
            files=request.FILES,
        )
        file = request.FILES.get('file')
        results = process_file(file)
        context = {
            'results': results,
            'form': form
        }
        return render(request, template, context)
    else:
        form = ReadFileForm(
            request.POST,
            files=request.FILES,
        )
        context = {
            'form': form
        }
        return render(request, template, context)
