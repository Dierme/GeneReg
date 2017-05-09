from request.lib.parsers import *
import requests


class AServiceHandler(ABC):

    _service_name = None
    _base_link = None

    def service_name(self):
        return self._service_name

    @abstractmethod
    def request(self, link, params):
        """Makes request TargetScan`.
            :param link: str
            :param params: dict
        """
        pass

    @abstractmethod
    def process_genes(self, genes_list):
        """Calsulates gene mirna`.
           :param genes_list: list
        """
        pass


class TargetScanHandler(AServiceHandler):

    _VIEW_GENE_CGI = 'view_gene.cgi'
    _VIEW_GENE_TXT_CGI = 'view_gene_text.cgi'
    _TARGETSCAN_CGI = 'targetscan.cgi'

    _VERSION = '/cgi-bin/targetscan/vert_71/'

    _SPECIES = 'Human'
    _TAXID = '9606'

    @staticmethod
    def _get_error_message(error_code, gene):
        return {
            1: 'Gene "%s" not found. Please, check that the name is correct.' % gene,
        }.get(error_code, 'Error message not found. Error code - %s' % error_code)

    def __init__(self):
        """Constructs a :class:`TargetScanParser <TargetScanParser>`.
           :param response: requests.Response
        """
        self._service_name = 'TargetScan'
        self._base_link = 'http://www.targetscan.org'
        self._parser = self.get_parser()
        self._rs = None

    @staticmethod
    def get_parser():
        return TargetScanParser()

    def process_genes(self, genes_list):

        parser = self.get_parser()

        result = {'gene_mirna_dict': dict(), 'warnings': dict()}

        gene_mirna_dict = dict()

        for gene in genes_list:
            self._rs = None
            kwargs = {'gene': gene, 'specification': None}
            response = self.request_builder(kwargs)
            parse_result = parser.parse(response)

            while not parse_result['success'] is True:
                kwargs = {'specification': parse_result['specification'], 'response': response}
                response = self.request_builder(kwargs)
                parse_result = parser.parse(response)

            if 'warning' in parse_result:
                result['warnings'][gene] = self._get_error_message(parse_result['warning'], gene)

            result['gene_mirna_dict'][gene] = parse_result['mirna_list']

        return result

    def request_builder(self, kwargs):
        if kwargs['specification'] is None:
            # make basic request to service
            params = {'params': {'species': self._SPECIES, 'gid': kwargs['gene']}}
            link = self._base_link + self._VERSION + self._TARGETSCAN_CGI

            response = requests.request('GET', link, **params)
            return response

        elif kwargs['specification'] == 1:
            # multiple builds. Make request for the first
            first_build_link = self._parser.find_first_link(kwargs['response'])
            self._rs = self._parser.get_rs_from_link(first_build_link)

            link = self._base_link + self._VERSION + self._VIEW_GENE_CGI
            params = {'rs': self._rs, 'taxid': self._TAXID, 'subset': '1'}
            response = self.request(link, params)
            return response

        elif kwargs['specification'] == 2:
            # get txt file
            # first check rs
            if self._rs is None:
                self._rs = self._parser.get_rs_from_download_table(kwargs['response'])

            # second sent request to create txt on server
            link = self._base_link + self._VERSION + self._VIEW_GENE_TXT_CGI
            params = {'rs': self._rs, 'taxid': self._TAXID}
            response = self.request(link, params)

            # third get .txt file
            link_to_txt = self._base_link + self._parser.find_first_link(response)
            response_txt = self.request(link_to_txt)
            return response_txt
        elif kwargs['specification'] == 3:
            # gene is not found
            return None

    def request(self, link, params=None):
        kwargs = {}
        if params is not None:
            kwargs = {'params': params}
        return requests.request('GET', link, **kwargs)




