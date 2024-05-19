# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, except_orm


class A4I_vehiclefleetmanager_vehicle_accident(models.Model):
    _name = 'a4i.vehiclefleetmanager.vehicle.accident'
    _description = 'Vehicle accidents'

    """
    Vehicle accidents
    """

    # State selection
    @api.model
    def _get_state(self):
        """
        Return the list of states
        :return: list
        """
        return [('draft', _('Draft')), ('declared', _('Declared')), ('in_expertise', _('In expertise')),
                ('in_reparation', _('Under reparation')), ('done', _('Done'))]

    # Type selection
    @api.model
    def _get_type(self):
        """
        Return the list of types
        :return: list
        """
        return [('accident', _('Accident')), ('theft', _('Theft')), ('fire', _('Fire')),
                ('weather', _('Weather damage')), ('other', _('Other'))]

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', required=True)
    state = fields.Selection(selection='_get_state', string='State', default='draft')
    type = fields.Selection(selection='_get_type', string='Type')
    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle')
    driver_id = fields.Many2one('a4i.vehiclefleetmanager.driver', string='Driver')
    accident_date = fields.Date(string='Accident date')
    accident_location = fields.Char(string='Accident location')
    declaration_date = fields.Date(string='Declaration date')
    expertise_date = fields.Date(string='Expertise date')
    reparation_date = fields.Date(string='Reparation date')
    insurance_company = fields.Many2one('res.partner', domain=[('is_supplier', '=', True)])
    reparation_amount = fields.Float(string='Reparation amount')
    deductible_amount = fields.Float(string='Deductible amount')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, ondelete='restrict', default=lambda self: self.env.user.company_id.currency_id)
    document_ids = fields.Many2many('document.openprod', 'a4i_vehiclefleetmanager_vehicle_accident_rel', string='Documents')
    internal_note = fields.Text(string='Internal notes')

    # ===========================================================================
    # METHODS
    # ===========================================================================

    @api.multi
    def wkf_draft(self):
        """
        Set the accident as draft
        """
        for accident_rc in self:
            accident_rc.write({'state': 'draft'})

    @api.multi
    def wkf_declared(self):
        """
        Set the accident as declared
        """
        for accident_rc in self:
            accident_rc.write({'state': 'declared'})

    @api.multi
    def wkf_in_expertise(self):
        """
        Set the accident as in expertise
        """
        for accident_rc in self:
            accident_rc.write({'state': 'in_expertise'})

    @api.multi
    def wkf_in_expertise(self):
        """
        Set the accident as in expertise
        """
        for accident_rc in self:
            accident_rc.write({'state': 'in_expertise'})

    @api.multi
    def wkf_in_reparation(self):
        """
        Set the accident as in reparation
        """
        for accident_rc in self:
            accident_rc.write({'state': 'in_reparation'})

    @api.multi
    def wkf_done(self):
        """
        Set the accident as done
        """
        for accident_rc in self:
            accident_rc.write({'state': 'done'})
