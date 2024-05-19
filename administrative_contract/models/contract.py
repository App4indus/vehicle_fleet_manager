# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, except_orm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.addons.base_openprod.common import get_form_view

import logging

LOG = logging.getLogger("dicttoxml")


class A4I_administrative_contract(models.Model):
    _name = 'a4i.administrative.contract'
    _description = 'Administrative contract'

    """
    Administrative contracts
    """

    # State selection
    @api.model
    def _get_state(self):
        """
        Return the state selection
        :return: list
        """
        return [('draft', _('Draft')), ('waiting', _('Waiting')), ('in_progress', _('In progress')),
                ('to_cancel', _('To cancel')), ('expired', _('Expired'))]

    # Frequency selection
    @api.model
    def _get_frequency(self):
        """
        Return the frequency selection
        :return: list
        """
        return [('daily', _('Daily')), ('weekly', _('Weekly')), ('monthly', _('Monthly')),
                ('quarterly', _('Quarterly')), ('annually', _('Annually'))]

    # Compute invoices costs
    @api.one
    @api.depends('supplier_invoice_ids')
    def _compute_invoices_costs(self):
        """
        Compute the total cost of the invoices
        :return: float
        """
        for contract in self:
            total = sum(invoice.amount_untaxed for invoice in contract.supplier_invoice_ids)
            contract.invoices_cost = total

    # Compute total costs
    @api.one
    @api.depends('application_cost', 'supplier_invoice_ids')
    def _compute_total_costs(self):
        """
        Compute the total cost of the contract
        :return: float
        """
        for contract in self:
            application_cost = contract.application_cost or 0
            invoices_cost = contract.invoices_cost or 0

            contract.total_cost = application_cost + invoices_cost

    # Compute actions nb
    @api.one
    def _compute_nb_actions(self):
        """
        Compute the number of actions
        :return: int
        """
        for contract in self:
            contract.nb_actions = self.env['calendar.event'].search_count(
                [('x_administrative_contract_id', '=', contract.id)])

    @api.one
    def _compute_next_action(self):
        """
        Compute the next action
        :return: dict
        """
        res_value = self.env['calendar.event'].search([('x_administrative_contract_id', '=', self.id)]).get_next_action_info(
            ['next_action', 'next_action_icon', 'next_action_date', 'next_action_label', 'next_action_color'])
        for k, v in res_value.iteritems():
            self[k] = v

    # ===========================================================================
    # ONCHANGES
    # ===========================================================================

    @api.onchange('reminder')
    def _onchange_reminder(self):
        """
        On change reminder
        :return: None
        """
        if self.reminder:
            if not self.reminder_date and self.end_date:
                self.reminder_date = datetime.strptime(self.end_date, '%Y-%m-%d') - timedelta(
                    days=(self.notice_days + 30))

            if not self.reminder_recipient_id:
                self.reminder_recipient_id = self.responsible_id.id

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    state = fields.Selection(selection='_get_state', string='State', default='draft', help='State of the contract')
    name = fields.Char(string='Name', help='Name of the contract')
    contract_reference = fields.Char(string='Contract reference', help='Reference of the contract')
    responsible_id = fields.Many2one('res.users', string='Responsible', help='Responsible of the contract')
    partner_id = fields.Many2one('res.partner', string='Partner', help='Partner linked the contract', ondelete='restrict')
    type_id = fields.Many2one('a4i.administrative.contract.type', string='Type', help='Type of the contract', ondelete='restrict')
    start_date = fields.Date(string='Start date', help='Start date of the contract')
    end_date = fields.Date(string='End date', help='End date of the contract')
    reminder = fields.Boolean(string='Reminder',
                              help='Reminder to stop the contract. If enabled, an action will be sent to the recipient.')
    reminder_ok = fields.Boolean(string='Reminder created', default=False, copy=False, help='Reminder created')
    reminder_date = fields.Date(string='Reminder date', help='Reminder date to stop the contract')
    reminder_recipient_id = fields.Many2one('res.users', string='Reminder recipient', help='Recipient of the reminder', ondelete='restrict')
    automatic_renewal = fields.Boolean(string='Automatic renewal', help='Automatic renewal of the contract')
    notice_days = fields.Integer(string='Notice (days)', help='Notice in days')
    periodical_cost = fields.Float(string='Periodical cost', help='Periodical cost of the contract')
    total_cost = fields.Float(string='Total cost', compute='_compute_total_costs', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, ondelete='cascade',
                                  default=lambda self: self.env.user.company_id.currency_id, help='Currency of the contract')
    periodical_cost_frequency = fields.Selection(selection='_get_frequency', string='Frequency periodical cost')
    application_cost = fields.Float(string='Initial application fees',
                                    help='Initial cost fees for the application of the contract')
    document_ids = fields.Many2many('document.openprod', 'a4i_administrative_contract_doc_rel', string='Documents', help='Documents related to the contract')
    internal_note = fields.Text(string='Internal notes')
    supplier_invoice_ids = fields.One2many('account.invoice', 'x_administrative_contract', string='Supplier invoices', help='Supplier invoices related to the contract')
    invoices_cost = fields.Float(compute='_compute_invoices_costs', string='Costs from invoices', help='Total cost of the invoices')
    actions_ids = fields.One2many('calendar.event', 'x_administrative_contract_id', comy=False, ondelete='set null', help='Actions related to the contract')
    nb_actions = fields.Integer(string='Actions', default=0, required=False, compute='_compute_nb_actions',
                                store=False, copy=False, help='Number of actions related to the contract')
    next_action = fields.Many2one('calendar.event', string='Next action', compute='_compute_next_action',
                                  required=False, store=False, help='Next action related to the contract')
    next_action_icon = fields.Char(string='Icon', compute='_compute_next_action', store=False, help='Icon of the next action')
    next_action_user_id = fields.Many2one('res.users', string='Next action responsible', required=False,
                                          ondelete='set null', compute='_compute_next_action', help='Responsible of the next action')
    next_action_date = fields.Date(string='Next action date', compute='_compute_next_action', help='Date of the next action', store=False)
    next_action_label = fields.Char(string='Next action', compute='_compute_next_action', store=False, help='Label of the next action')
    next_action_color = fields.Char(string='Next action color', default='', compute='_compute_next_action', store=False, help='Color of the next action')

    # ===========================================================================
    # METHODS
    # ===========================================================================

    @api.multi
    def wkf_draft(self):
        """
        Set the contract to draft state
        :return: None
        """
        for contract_rc in self:
            contract_rc.write({'state': 'draft'})

    @api.multi
    def wkf_waiting(self):
        """
        Set the contract to waiting state
        :return: None
        """
        for contract_rc in self:
            contract_rc.write({'state': 'waiting'})

    @api.multi
    def wkf_in_progress(self):
        """
        Set the contract to in progress state
        :return: None
        """
        for contract_rc in self:
            contract_rc.write({'state': 'in_progress'})

    @api.multi
    def wkf_to_cancel(self):
        """
        Set the contract to to cancel state
        :return: None
        """
        for contract_rc in self:
            contract_rc.write({'state': 'to_cancel'})

    @api.multi
    def wkf_expired(self):
        """
        Set the contract to expired state
        :return: None
        """
        for contract_rc in self:
            contract_rc.write({'state': 'expired'})

    @api.multi
    def add_manual_cost(self):
        """
        Add manual cost
        :return: dict
        """

        wiz_obj = self.env['a4i.administrative.contract.add.cost']

        for contract_rc in self:
            vals_wiz = {'contract_id': contract_rc.id}
            wiz_rc = wiz_obj.create(vals_wiz)
            return {
                'name': _('Add manual cost'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': '4i.contract.administrative.add.cost',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': wiz_rc.id,
                'nodestroy': True,
            }

    @api.multi
    def affect_account_invoices(self):
        """
        Affect account invoices to the contract
        :return: dict
        """

        wiz_obj = self.env['a4i.administrative.contract.invoice.add']

        for contract_rc in self:
            vals_wiz = {'contract_id': contract_rc.id}
            wiz_rc = wiz_obj.create(vals_wiz)
            return {
                'name': _('Affect invoice to the contract'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'a4i.administrative.contract.invoice.add',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': wiz_rc.id
            }

    @api.multi
    def cron_create_reminder(self):
        """
        Create a reminder to stop the contract
        :return: bool
        """

        action_obj = self.env['calendar.event']
        data_obj = self.env['ir.model.data']

        object_model, action_type_id = data_obj.get_object_reference('base_openprod', 'simple_action_type_action')
        state_action_rs = self.env['action.state'].search([('to_do_state', '=', True)], limit=1)

        contract_to_reminder_rcs = self.search([('reminder', '=', True), ('reminder_ok', '=', False)])

        for contract_rc in contract_to_reminder_rcs:
            if contract_rc.reminder_date <= fields.Date.today():
                vals = {
                    'name': _('Reminder to stop contract : [{partner_name}] {contract_name} '.format(
                        partner_name=contract_rc.partner_id.name, contract_name=contract_rc.name)),
                    'description': _('A reminder was created to stop the mentioned contract.'),
                    'start_datetime': contract_rc.reminder_date,
                    'stop_datetime': contract_rc.reminder_date,
                    'user_id': contract_rc.reminder_recipient_id.id,
                    'confidentiality': 'responsible',
                    'origin': 'other',
                    'priority': '4',
                    'affected_user_id': contract_rc.reminder_recipient_id.id,
                    'state_id': state_action_rs.id,
                    'type_id': action_type_id,
                    'x_administrative_contract_id': contract_rc.id
                }
                action_rc = action_obj.create(vals)
                if action_rc:
                    contract_rc.reminder_ok = True

        return True

    @api.multi
    def cron_generate_automatic_costs(self):
        """
        Generate automatic costs, based on periodical costs
        :return: None
        """

        cost_obj = self.env['a4i.administrative.contract.cost']
        contracts_rcs = self.search([('state', '=', 'in_progress')])
        for contract_rc in contracts_rcs:

            # Generate initial cost
            if contract_rc.application_cost:
                cost_rc = cost_obj.search([('contract_id', '=', contract_rc.id), ('type', '=', 'initial')], limit=1)

                if cost_rc:
                    cost_rc.amount = contract_rc.application_cost
                else:
                    cost_vals = {
                        'name': 'Initial Cost',
                        'type': 'initial',
                        'amount': contract_rc.application_cost,
                        'contract_id': contract_rc.id,
                        'date': contract_rc.start_date,
                    }

                    cost_obj.create(cost_vals)

            # Generate periodical cost
            if contract_rc.periodical_cost:
                today = datetime.now()
                start_date = contract_rc.periodical_cost_last_due_date or contract_rc.periodical_cost_start_date
                start_date = datetime.strptime(start_date, '%Y-%m-%d')

                date_due = start_date
                while date_due <= today:

                    cost_vals = {
                        'name': 'Recurring Cost',
                        'type': 'periodic',
                        'amount': contract_rc.periodical_cost,
                        'contract_id': contract_rc.id,
                        'date': date_due,
                    }

                    cost_rc = cost_obj.create(cost_vals)
                    if cost_rc:
                        start_date = date_due
                        contract_rc.periodical_cost_last_due_date = date_due

                    if contract_rc.periodical_cost_frequency == 'monthly':
                        date_due += relativedelta(months=1)
                    elif contract_rc.periodical_cost_frequency == 'quarterly':
                        date_due = start_date + timedelta(days=120)
                    elif contract_rc.periodical_cost_frequency == 'annually':
                        date_due = start_date + timedelta(days=365)

    @api.multi
    def create_action(self):
        """
        Create an action
        :return: dict
        """
        action_obj = self.env['calendar.event']
        data_obj = self.env['ir.model.data']

        object_model, action_type_id = data_obj.get_object_reference('base_openprod', 'simple_action_type_action')
        state_action_rs = self.env['action.state'].search([('to_do_state', '=', True)], limit=1)
        for contract_rc in self:

            vals = {
                'name': _('Action from contract : [{partner_name}] {contract_name} '.format(
                    partner_name=contract_rc.partner_id.name, contract_name=contract_rc.name)),
                'start_datetime': fields.Date.today(),
                'stop_datetime': fields.Date.today(),
                'user_id': contract_rc.reminder_recipient_id.id,
                'confidentiality': 'responsible',
                'origin': 'other',
                'priority': '2',
                'affected_user_id': contract_rc.reminder_recipient_id.id,
                'state_id': state_action_rs.id,
                'type_id': action_type_id,
                'x_administrative_contract_id': contract_rc.id

            }

            new_action_rc = action_obj.create(vals)
            if new_action_rc:
                action_struc = {}
                action_dict = get_form_view(self, 'base_openprod.action_see_one_action')
                if action_dict and action_dict.get('id') and action_dict.get('type'):
                    action = self.env[action_dict['type']].browse(action_dict['id'])
                    action_struc = action.read()
                    action_struc[0]['res_id'] = new_action_rc.id
                    action_struc = action_struc[0]
                    return action_struc

    @api.multi
    def show_actions(self):
        """
        Show actions
        :return: dict
        """

        act_dict = self.env.ref('base_openprod.action_user_my_action').read()[0]
        act_dict['domain'] = [('x_administrative_contract_id', 'in', self.ids)]
        return act_dict

    @api.multi
    def button_next_action_purchase(self):
        """
        Button next action purchase
        :return: dict
        """
        action_dict = get_form_view(self, 'base_openprod.action_user_action_target_new')
        for purchase in self:
            action_struc = {}
            if action_dict and action_dict.get('id') and action_dict.get('type') and purchase.next_action: # existing action
                action = self.env[action_dict['type']].browse(action_dict['id'])
                action_struc = action.read()
                action_struc[0]['name'] = _(u"Next action")
                action_struc[0]['res_id'] = purchase.next_action.id
                action_struc[0]['context'] = {
                    'default_button_save_visible_wiz': True, # True : show Save+Cancel
                }
                action_struc = action_struc[0]
                return action_struc

    @api.multi
    def show_invoices(self):
        """
        Show invoices
        :return: dict
        """
        act_dict = self.env.ref('account.action_invoice_tree2').read()[0]
        act_dict['domain'] = [('x_administrative_contract', '=', self.id)]
        return act_dict


class A4I_administrative_contract_type(models.Model):
    _name = 'a4i.administrative.contract.type'
    _description = 'Administrative contract type'

    """
    Administrative contract types
    """

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', help='Name of the type')
