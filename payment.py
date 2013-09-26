## coding: utf-8
# This file is part of account_payment_es_csb_19 module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
import logging
try:
    from retrofix import Record, write, c19
except ImportError:
    message = ('Unable to import retrofix library.\n'
               'Please install it before install this module.')
    logging.getLogger('account_payment_es_csb_19').error(message)
    raise Exception(message)

__all__ = [
    'Journal',
    'Group',
    ]
__metaclass__ = PoolMeta


class Journal:
    __name__ = 'account.payment.journal'
    csb19_extra_concepts = fields.Boolean('Extra Concepts',
        help=('Check it if you want to add the invoice lines to the extra '
            'concepts (Max. 15 lines).\nAnnex 2 of CSB 19 norm.'))
    csb19_add_address = fields.Boolean('Add address',
        help=('Check it if you want to add the domicile of the owner of the '
            'bank account to the file.\nAnnex 3 of CSB 19 norm.'))

    @classmethod
    def __setup__(cls):
        super(Journal, cls).__setup__()
        if ('csb19', 'CSB 19') not in cls.process_method.selection:
            cls.process_method.selection.extend([
                ('csb19', 'CSB 19'),
                ])


class Group:
    __name__ = 'account.payment.group'

    def set_default_csb19_payment_values(self):
        values = self.set_default_payment_values()
        values['extra_concepts'] = values['payment_journal'].\
            csb19_extra_concepts
        values['add_address'] = values['payment_journal'].csb19_add_address
        values['bank_account'] = values['bank_account'].numbers[0].number
        values['record_count'] = 0
        values['procedure'] = '01'
        values['ordering_count'] = 1
        values['required_count'] = 0
        for receipt in values['receipts']:
            if values['extra_concepts'] or values['add_address'] and not \
                    receipt['address']:
                self.raise_user_error('configuration_error',
                    error_description='party_without_address',
                    error_description_args=(receipt['name'],))
            receipt['bank_account'] = receipt['bank_account'].numbers[0].number
            receipt['party_code'] = receipt['party'].code
        return values

    @classmethod
    def process_csb19(cls, group):

        def set_presenter_header_record():
            record = Record(c19.PRESENTER_HEADER_RECORD)
            record.record_code = '51'
            record.data_code = '80'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.creation_date = values['creation_date']
            record.name = values['company_name']
            record.bank_code = values['bank_account'][0:4]
            record.bank_office = values['bank_account'][4:8]
            return write([record])

        def set_ordering_header_record():
            record = Record(c19.ORDERING_HEADER_RECORD)
            record.record_code = '53'
            record.data_code = '80'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.creation_date = values['creation_date']
            record.payment_date = values['payment_date']
            record.name = values['company_name']
            record.account = values['bank_account']
            record.procedure = values['procedure']
            return write([record])

        def set_required_individual_record():
            record = Record(c19.REQUIRED_INDIVIDUAL_RECORD)
            record.record_code = '56'
            record.data_code = '80'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.reference_code = receipt['party_code']
            record.name = receipt['name']
            record.account = receipt['bank_account']
            record.amount = receipt['amount']
            record.concept = receipt['communication']
            return write([record])

        def set_first_optional_individual_record():
            record = Record(c19.FIRST_OPTIONAL_INDIVIDUAL_RECORD)
            record.record_code = '56'
            record.data_code = '81'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.reference_code = receipt['party_code']
            record.second_field_concept = field['second_field_concept']
            record.third_field_concept = field['third_field_concept']
            record.fourth_field_concept = field['fourth_field_concept']
            return write([record])

        def set_second_optional_individual_record():
            record = Record(c19.SECOND_OPTIONAL_INDIVIDUAL_RECORD)
            record.record_code = '56'
            record.data_code = '82'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.reference_code = receipt['party_code']
            record.fifth_field_concept = field['fifth_field_concept']
            record.sixth_field_concept = field['sixth_field_concept']
            record.seventh_field_concept = field['seventh_field_concept']
            return write([record])

        def set_third_optional_individual_record():
            record = Record(c19.THIRD_OPTIONAL_INDIVIDUAL_RECORD)
            record.record_code = '56'
            record.data_code = '83'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.reference_code = receipt['party_code']
            record.eighth_field_concept = field['eighth_field_concept']
            record.ninth_field_concept = field['ninth_field_concept']
            record.tenth_field_concept = field['tenth_field_concept']
            return write([record])

        def set_fourth_optional_individual_record():
            record = Record(c19.FOURTH_OPTIONAL_INDIVIDUAL_RECORD)
            record.record_code = '56'
            record.data_code = '84'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.reference_code = receipt['party_code']
            record.eleventh_field_concept = field['eleventh_field_concept']
            record.twelfth_field_concept = field['twelfth_field_concept']
            record.thirteenth_field_concept = field['thirteenth_field_concept']
            return write([record])

        def set_fifth_optional_individual_record():
            record = Record(c19.FIFTH_OPTIONAL_INDIVIDUAL_RECORD)
            record.record_code = '56'
            record.data_code = '85'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.reference_code = receipt['party_code']
            record.fourteenth_field_concept = field['fourteenth_field_concept']
            record.fifteenth_field_concept = field['fifteenth_field_concept']
            record.sixteenth_field_concept = field['sixteenth_field_concept']
            return write([record])

        def set_sixth_optional_individual_record():
            record = Record(c19.SIXTH_OPTIONAL_INDIVIDUAL_RECORD)
            record.record_code = '56'
            record.data_code = '86'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.reference_code = receipt['party_code']
            record.name = receipt['name']
            record.address = receipt['address'].street
            record.city = receipt['address'].city
            record.zip = receipt['address'].zip
            return write([record])

        def set_ordering_footer_record():
            record = Record(c19.ORDERING_FOOTER_RECORD)
            record.record_code = '58'
            record.data_code = '80'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.amount_sum = values['amount']
            record.required_count = str(values['required_count'])
            record.record_count = str(values['record_count'])
            return write([record])

        def set_presenter_footer_record():
            record = Record(c19.PRESENTER_FOOTER_RECORD)
            record.record_code = '59'
            record.data_code = '80'
            record.nif = values['vat_number']
            record.suffix = values['suffix']
            record.ordering_count = str(values['ordering_count'])
            record.amount_sum = values['amount']
            record.required_count = str(values['required_count'])
            record.record_count = str(values['record_count'])
            return write([record])

        values = Group.set_default_csb19_payment_values(group)
        keys = (
            'second_field_concept',
            'third_field_concept',
            'fourth_field_concept',
            'fifth_field_concept',
            'sixth_field_concept',
            'seventh_field_concept',
            'eighth_field_concept',
            'ninth_field_concept',
            'tenth_field_concept',
            'eleventh_field_concept',
            'twelfth_field_concept',
            'thirteenth_field_concept',
            'fourteenth_field_concept',
            'fifteenth_field_concept',
            'sixteenth_field_concept',
            )
        field = {key: '' for key in keys}

        text = set_presenter_header_record() + '\r\n'
        values['record_count'] += 1
        text += set_ordering_header_record() + '\r\n'
        values['record_count'] += 1
        for receipt in values['receipts']:
            values['required_count'] += 1
            text += set_required_individual_record() + '\r\n'
            values['record_count'] += 1
            if values['extra_concepts']:
                concepts = []
                for invoice in receipt['invoices']:
                    for line in invoice.lines:
                        amount = ' %(#).2f ' % {'#': line.amount}
                        concepts.append('%s %s' % (line.description,
                                amount.replace('.', ',')))
                for (key, receipt['communication']) in zip(keys, concepts):
                    field[key] = receipt['communication']
                if field['second_field_concept']:
                    text += set_first_optional_individual_record() + '\r\n'
                    values['record_count'] += 1
                if field['fifth_field_concept']:
                    text += set_second_optional_individual_record() + '\r\n'
                    values['record_count'] += 1
                if field['eighth_field_concept']:
                    text += set_third_optional_individual_record() + '\r\n'
                    values['record_count'] += 1
                if field['eleventh_field_concept']:
                    text += set_fourth_optional_individual_record() + '\r\n'
                    values['record_count'] += 1
                if field['fourteenth_field_concept']:
                    text += set_fifth_optional_individual_record() + '\r\n'
                    values['record_count'] += 1
                text += set_sixth_optional_individual_record() + '\r\n'
                values['record_count'] += 1
            elif values['add_address']:
                text += set_sixth_optional_individual_record() + '\r\n'
                values['record_count'] += 1
        text += set_ordering_footer_record() + '\r\n'
        values['record_count'] += 2
        text += set_presenter_footer_record()
        group.attach_file(text)
