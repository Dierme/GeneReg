
class Validate(object):

    def __init__(self, form_data):
        self.not_blank_fields = ['genes']
        self.form_fields = ['genes', 'min_genes', 'min_sites', 'service']
        self.digit_fields = ['min_genes', 'min_sites', 'service']
        self.form_data = form_data
        self.errors = list()

    def validate(self):
        for field in self.not_blank_fields:
            self.is_set(field)

        for field in self.form_fields:
            self.is_blank(field)

        for field in self.digit_fields:
            self.is_digit(field)

        if not self.errors:
            if len(self.form_data['genes'].split(',')) < int(self.form_data['min_genes']):
                self.errors.append('Min number of genes can not be more that total amount of genes')

        return self.errors

    def is_blank(self, field_name):
        if self.form_data[field_name] == '':
            self.errors.append('Param %s should not be blank' % field_name)

    def is_set(self, field_name):
        if field_name not in self.form_data:
            self.errors.append('Param %s is missing' % field_name)

    def is_digit(self, field_name):
        if not self.form_data[field_name].isdigit():
            self.errors.append('Param %s must be digit' % field_name)
