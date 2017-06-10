from abc import ABC, abstractmethod, abstractproperty
from tarfind.src.utulity import Utility
import time


class AParser(ABC):

    @abstractproperty
    def service_name(self):
        pass

    @abstractmethod
    def parse(self, response):
        pass


class TargetScanParser(AParser):

    _ADD_SELECTION_STR_1 = 'corresponds to multiple transcripts'
    _ADD_SELECTION_STR_2 = 'Choose one to see in detail'
    _ADD_SELECTION_EXT = '.txt'

    _GENE_NOT_IN_DB1 = 'A gene of this name'
    _GENE_NOT_IN_DB2 = 'is not in our UTR database.'

    _ANCHOR_FIRST_BUILD1 = '<A HREF="'
    _ANCHOR_FIRST_BUILD2 = '"'

    _ANCHOR_DOWNLOAD_TABLE1 = 'view_gene_text.cgi?'
    _ANCHOR_DOWNLOAD_TABLE2 = '"'

    _DELAY1 = 'Creating an image map for'
    _DELAY2 = '....please wait'

    _RESULT_PAGE1 = '<H3>Conserved</H3>'
    _RESULT_PAGE2 = '<H3>Poorly conserved</H3>'

    _ERROR_GENE_NOT_FOUND = 1

    def __init__(self):
        self._service_name = 'TargetScan'
        self.response = None

    def service_name(self):
        return self._service_name

    def find_first_link(self, response):
        """Selects the first build from TargetScan response
           :param response: requests.Response
        """
        link = Utility.cut_string(response.text, self._ANCHOR_FIRST_BUILD1, self._ANCHOR_FIRST_BUILD2)
        return link

    def get_rs_from_download_table(self, response):
        """Gets rs from raw page code
           :param response: requests.Response
        """
        # if response is "please wait" page
        if self._DELAY1 in response.text and self._DELAY2 in response.text:
            rs = Utility.cut_string(response.text, self._DELAY1, self._DELAY2)
            return rs.strip()

        # if response is image map
        link = Utility.cut_string(response.text, self._ANCHOR_DOWNLOAD_TABLE1, self._ANCHOR_DOWNLOAD_TABLE2)
        return link.split('&')[1].split('=')[1]


    def get_rs_from_link(self, link):
        """Cuts rs from target scan link
           :param link: string
        """
        return link.split('?')[1].split('&')[0].split('=')[1]

    def additional_selection_needed(self):
        response_text = self.response.text

        if self._ADD_SELECTION_STR_1 in response_text and self._ADD_SELECTION_STR_2 in response_text:
            # !There are multiple builds for gene. Choose the first option
            # ideally make representation of choices to the user
            return 1
        elif self._RESULT_PAGE1 in response_text and self._RESULT_PAGE2 in response_text:
            # make request for txt file
            return 2
        elif self._DELAY1 in response_text and self._DELAY2 in response_text:
            # TacrgetScan created image map. Repeat step2
            time.sleep(2)
            return 2
        elif self._GENE_NOT_IN_DB1 in response_text and self._GENE_NOT_IN_DB2:
            # gene not found in TargetScan
            return 3
        elif self._ADD_SELECTION_EXT in self.response.url:
            # file is .txt . May be parsed
            return None
        else:
            raise Exception('Something went astray determining page %s' % self.response.url)

    def parse(self, response):
        """Parses response from request to TargetScan
           :param response: requests.Response
        """
        if response is None:
            return {
                'success': True,
                'specification': None,
                'mirna_list': {},
                'warning': self._ERROR_GENE_NOT_FOUND
            }

        self.response = response
        specification = self.additional_selection_needed()
        if specification is not None:
            return {'success': False, 'specification': specification}

        # parsing txt response file
        file = response.text
        lines = file.splitlines()
        mirna_dict = dict()

        mirna_params = lines[0].split('\t')
        lines = lines[1:]

        for i, line in enumerate(lines):
            line_list = list()
            line_split_space = line.split(' ')
            for line_part in line_split_space:
                line_list += line_part.split('\t')

            # work with not conserved sites is not implemented yet
            if line_list[0] == 'Poorly':
                break

            # working with conserved sites
            if line_list[0] == 'Conserved':
                continue
            mirna_name = line_list[0]
            if mirna_name in mirna_dict:
                mirna_dict[mirna_name] += 1
            else:
                mirna_dict[mirna_name] = 1

        return {'success': True, 'specification': None, 'mirna_list': mirna_dict}




