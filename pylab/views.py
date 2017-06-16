from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from random import randint
import json
from .models import Names
from .forms import NamesForm
from django.utils import timezone

# Create your views here.


def index(request):
    # n = Names(name="Dima", pub_date=timezone.now())
    # n.save()
    context = {'names': Names.objects.all(), 'form': NamesForm()}
    return render(request, 'pylab/index.html', context)


def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        response_data = {}

        form = NamesForm(request.POST)
        if form.is_valid():
            response_data['success'] = True
            n = Names(name=name, pub_date=timezone.now())
            n.save()
            response_data['new_names_html'] = render_to_string('pylab/_names_table.html', {
                'names':  Names.objects.all()})

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            response_data['success'] = False
            response_data['errors'] = form.errors
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def delete(request):
    response_data = {}

    if request.method == 'POST':
        name_id = int(request.POST.get('id'))
        if Names.objects.filter(id=name_id).exists():
            response_data['success'] = True
            name = Names.objects.filter(id=name_id)
            name.delete()
            response_data['new_names_html'] = render_to_string('pylab/_names_table.html', {
                'names': Names.objects.all()})
        else:
            response_data['success'] = False
            response_data['errors'] = {'Names': ['object not found']}
    else:
        response_data['success'] = False
        response_data['errors'] = {'Request': ['Is not post']}

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


def random(request):
    response_data = dict()
    if request.method == 'POST':

        names_queryset = Names.objects.all()
        ln = len(names_queryset)

        if ln < 3:
            response_data['success'] = False
            response_data['errors'] = {'Names': ['Names number should be 3 or more']}
        else:
            names = list()
            for element in names_queryset:
                names.append(element.name)
            chosen_names = list()
            for i in range(0, 3):
                rand_name_idx = randint(0, ln - 1)
                chosen_names.append(names[rand_name_idx])
                names.pop(rand_name_idx)
                ln = len(names)

            response_data['success'] = True
            response_data['chosen_names_html'] = render_to_string('pylab/_rand_names.html', {
                'chosen_names': chosen_names})
    else:
        response_data['success'] = False
        response_data['errors'] = {'Request': ['Is not post']}

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


