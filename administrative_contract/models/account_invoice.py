# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class a4i_administrative_contract_invoice(models.Model):
    _inherit = 'account.invoice'

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    x_administrative_contract = fields.Many2one('a4i.administrative.contract', string='Administrative contract', copy=False, help='Administrative contract related to this invoice')
