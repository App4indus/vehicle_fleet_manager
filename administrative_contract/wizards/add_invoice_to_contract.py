# -*- coding: utf-8 -*-
import openerp
from openerp.exceptions import except_orm, ValidationError
from openerp import _, api, fields, models


class A4I_administrative_contract_add_invoice(models.TransientModel):
    """
        Wizard to add invoice cost to contract
    """
    _name = 'a4i.administrative.contract.invoice.add'
    _description = "Add invoice to contract"

    # ===========================================================================
    # ON CHANGES
    # ===========================================================================

    @api.onchange('amount_filter', 'expected_amount')
    def _onchange_amount_filter(self):
        # Dynamic domain
        domain = [('type', '=', 'in_invoice'), ('x_administrative_contract', '=', False)]
        if self.amount_filter:
            domain.append(('amount_untaxed', '=', self.expected_amount))
        return {'domain': {'account_invoice_ids': domain}}

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    contract_id = fields.Many2one('a4i.administrative.contract', string='Contract')
    account_invoice_ids = fields.Many2many('account.invoice', 'wizard_contract_add_invoice_account_invoice_rel',
                                           'wiz_id', 'account_invoice_id')
    expected_amount = fields.Float(related='contract_id.periodical_cost', string='Expected amount')
    amount_filter = fields.Boolean(string='Filter invoices with expected amount', default=True)

    # ===========================================================================
    # METHODS
    # ===========================================================================

    @api.multi
    def button_delete_lines(self):
        self.account_invoice_ids = False

        return {'type': 'ir.actions.act_window_dialog_reload'}

    @api.multi
    def validate(self):

        for invoice in self.account_invoice_ids:
            self.contract_id.supplier_invoice_ids = [(4, invoice.id)]

        return True
