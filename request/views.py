from django.shortcuts import render
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from .models import Services
from .forms.search_form import Validate
import json
import requests
from request.lib.service_handlers import TargetScanHandler

# Create your views here.


def index(request):
    if request.method == 'POST':

        validator = Validate(request.POST)
        errors = validator.validate()

        if errors:
            html = render_to_string('request/_error.html', {'errors': errors})
            return JsonResponse({'success': False, 'html': html})

        min_genes = int(request.POST['min_genes'])
        min_sites = int(request.POST['min_sites'])

        genes_list = list()
        genes = str(request.POST['genes']).split(',')

        for gene in genes:
            genes_list.append(gene)

        target_scan_handler = TargetScanHandler()
        response = target_scan_handler.process_genes(genes_list)

        final_mirna_dict = dict()
        for gene, mirna_dict in response['gene_mirna_dict'].items():
            for mirna, n_sites in mirna_dict.items():
                if mirna in final_mirna_dict:
                    final_mirna_dict[mirna]['genes_name'].append(gene)
                    final_mirna_dict[mirna]['sites'] += n_sites
                else:
                    final_mirna_dict[mirna] = {'sites': n_sites, 'genes_name': [gene]}

        html = render_to_string('request/_result.html', {
            'success': True,
            'final_mirna_dict': final_mirna_dict,
            'warnings': response['warnings'],
            'min_genes': min_genes,
            'min_sites': min_sites})

        return JsonResponse({'success': True, 'html': html})

    services = Services.objects.all()

    context = {'services': services}
    return render(request, 'request/index.html', context)
