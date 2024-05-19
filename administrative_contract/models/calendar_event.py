# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class a4i_administrative_contract_calendar_event(models.Model):
    _inherit = 'calendar.event'

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    x_administrative_contract_id = fields.Many2one('a4i.administrative.contract', string='Administrative contract', help='Administrative contract related to this event', copy=False)
