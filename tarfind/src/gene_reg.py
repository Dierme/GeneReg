import requests
from request.models import Services
from request.lib.parsers import *


class GeneReg(object):

    METHOD_GET = 'GET'

    def __init__(self, gene_list):
        self.gene_list = gene_list

    def process_genes_to_services(self):
        services = Services.objects.all()
        for gene in self.gene_list:
            for service in services:
                response = requests.request(self.METHOD_GET, service.base_url)