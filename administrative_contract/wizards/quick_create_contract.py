# -*- coding: utf-8 -*-
import openerp
from openerp.exceptions import except_orm, ValidationError
from openerp import _, api, fields, models


class A4I_administrative_contract_quick_add(models.TransientModel):
    """
        Wizard - quick create of contract
    """
    _name = 'a4i.administrative.contract.quick.create.wizard'
    _description = "Administrative contract - quick creation"

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', required=True)
    responsible_id = fields.Many2one('res.users', string='Responsible', help='Responsible of the contract', required=True)
    type_id = fields.Many2one('a4i.administrative.contract.type', string='Type')
    start_date = fields.Date(string='Start date', help='Start date of the contract')
    end_date = fields.Date(string='End date', help='End date of the contract')
    internal_note = fields.Text(string='Internal notes')

    @api.multi
    def create_contract(self):

        contract_vals = {'name': self.name, 'type_id': self.type_id.id,
                        'responsible_id': self.responsible_id.id, 'start_date': self.start_date,
                         'end_date': self.end_date, 'nternal_note': self.internal_note}

        contract_rc = self.env['a4i.administrative.contract'].create(contract_vals)
        if contract_rc:
            act_dict = self.env.ref('administrative_contract.act_contract_administrative_a4i').read()[0]
            act_dict['domain'] = [('id', '=', contract_rc.id)]
            return act_dict
