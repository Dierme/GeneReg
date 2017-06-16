from django.shortcuts import render

from request.lib.service_handlers import TargetScanHandler

# Create your views here.


def index(request):
    context = {}
    return render(request, 'pylab/index.html', context)
