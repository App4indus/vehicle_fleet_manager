# -*- coding: utf-8 -*-
import openerp
from openerp.exceptions import except_orm, ValidationError
from openerp import _, api, fields, models


class A4I_administrative_contract_add_cost(models.TransientModel):
    """
        Wizard to add cost to contract
    """
    _name = 'a4i.administrative.contract.add.cost'
    _description = "Enter manual cost"

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    contract_id = fields.Many2one('a4i.administrative.contract', string='Contract')
    amount = fields.Float(string='Amount')
    date = fields.Date(string='Date')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, ondelete='cascade', default=lambda self: self.env.user.company_id.currency_id)

    @api.multi
    def add_cost(self):
        for wiz_rc in self:
            if self.contract_id:
                cost_vals = {
                    'name': 'Manual cost',
                    'type': 'manual',
                    'amount': wiz_rc.amount,
                    'currency_id': wiz_rc.currency_id.id,
                    'contract_id': wiz_rc.contract_id.id,
                    'date': wiz_rc.date,
                }
                self.env['4i.contract.administrative.cost'].create(cost_vals)

            else:
                raise ValidationError(_("You must specify a contract"))
