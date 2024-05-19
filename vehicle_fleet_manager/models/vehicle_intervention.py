# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, except_orm


class A4I_vehiclefleetmanager_vehicle_intervention(models.Model):
    _name = 'a4i.vehiclefleetmanager.vehicle.intervention'
    _description = 'Vehicle interventions'

    """
    Vehicle interventions
    """

    # State selection
    @api.model
    def _get_state(self):
        """"
        Return the list of states
        :return: list
        """
        return [('requested', _('Requested')), ('planned', _('Planned')), ('in_progress', _('In progress')), ('done', _('Done'))]

    # Type selection
    @api.model
    def _get_type(self):
        """
        Return the list of types
        :return: list
        """
        return [('fixed', _('Fixed')), ('variable', _('Variable'))]

    @api.model
    def _get_months(self):
        """
        Return the list of months
        :return: list
        """
        return [
            ('01', _('January')),
            ('02', _('February')),
            ('03', _('March')),
            ('04', _('April')),
            ('05', _('May')),
            ('06', _('June')),
            ('07', _('July')),
            ('08', _('August')),
            ('09', _('September')),
            ('10', _('October')),
            ('11', _('November')),
            ('12', _('December'))
        ]

    @api.model
    def create(self, vals):
        """
        Override the create method to update the odometer
        :param vals: dict
        :return: recordset
        """
        rc = super(A4I_vehiclefleetmanager_vehicle_intervention, self).create(vals=vals)

        # Update odometer
        if rc.vehicle_id and rc.odometer:
            vals = {'vehicle_id': rc.vehicle_id.id, 'update_origin': "Intervention",
                    'odometer_value': rc.odometer, 'update_date': fields.datetime.now(),
                    'update_user_id': self.env.user.id}
            self.env['a4i.vehiclefleetmanager.vehicle.odometer'].create(vals)

        return rc

    @api.one
    @api.depends('planned_date', 'real_date')
    def _compute_date(self):
        """
        Compute the month and year of the intervention
        :return: None
        """
        date = False
        # On prend la date réelle
        if self.real_date:
            date = fields.Date.from_string(self.real_date)
        # Ou la date prévue
        elif self.planned_date:
            date = fields.Date.from_string(self.planned_date)

        else:
            self.month = False
            self.year = False

        if date:
            # On récupère le nom du jour et le numéro de l'année
            isocal = date.isocalendar()
            self.day = str(isocal[2])
            self.year = str(isocal[0])

            # On récupère le mois
            if len(str(date.month)) == 1:
                self.month = '0%s' % (str(date.month))
            else:
                self.month = str(date.month)

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    state = fields.Selection(selection='_get_state', string='State', default='requested')
    type_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle.intervention.type', string='Type')
    name = fields.Char(string='Name')
    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle')
    supplier_id = fields.Many2one('res.partner', string='Supplier', help='Partner who maintened the vehicle', domain="[('is_supplier', '=', True)]")
    document_ids = fields.Many2many('document.openprod', 'a4i_vehiclefleetmanager_vehicle_intervention_doc_rel', string='Documents')
    planned_date = fields.Date(string='Planned intervention date', required=True)
    real_date = fields.Date(string='Real intervention date')
    amount = fields.Float(string='Amount')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, ondelete='restrict', default=lambda self: self.env.user.company_id.currency_id)
    odometer = fields.Integer(string='Odometer', help='Odometer at intervention')
    internal_note = fields.Text(string='Internal notes')

    # Date
    month = fields.Selection(selection='_get_months', string='Month', compute='_compute_date', store=True)
    year = fields.Char(string='Year', size=4, compute='_compute_date', store=True)

    # ===========================================================================
    # METHODS
    # ===========================================================================

    @api.multi
    def wkf_requested(self):
        """
        Set the intervention as requested
        """
        for inter_rc in self:
            inter_rc.write({'state': 'requested'})

    @api.multi
    def wkf_planned(self):
        """
        Set the intervention as planned
        """
        for inter_rc in self:
            inter_rc.write({'state': 'planned'})

    @api.multi
    def wkf_in_progress(self):
        """
        Set the intervention as in progress
        """
        for inter_rc in self:
            inter_rc.write({'state': 'in_progress'})

    @api.multi
    def wkf_done(self):
        """
        Set the intervention as done
        """
        for inter_rc in self:
            inter_rc.write({'state': 'done'})


class A4I_vehiclefleetmanager_vehicle_intervention_type(models.Model):
    _name = 'a4i.vehiclefleetmanager.vehicle.intervention.type'
    _description = 'Vehicle intervention types'

    """
    Vehicle intervention types
    """

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name')
