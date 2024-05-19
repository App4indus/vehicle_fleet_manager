# -*- coding: utf-8 -*-
import openerp
from openerp.exceptions import except_orm, ValidationError
from openerp import _, api, fields, models
from openerp.exceptions import AccessDenied, UserError, AccessError
from openerp.http import request


class A4I_vehiclefleetmanager_accident_quick_add(models.TransientModel):
    """
        Wizard create accident quickly
    """
    _name = 'a4i.vehiclefleetmanager.accident.quick.create.wizard'
    _description = "Accident - quick creation"

    # Type selection
    @api.model
    def _get_type(self):
        return [('accident', _('Accident')), ('theft', _('Theft')), ('fire', _('Fire')),
                ('weather', _('Weather damage')), ('other', _('Other'))]

    @api.onchange('type', 'accident_date')
    def onchange_compute_name(self):
        name = ''
        if self.type:
            name += '%s' % (self.type)

        if self.accident_date:
            name += ' on %s' % (self.accident_date)

        self.name = name

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', required=True)
    type = fields.Selection(selection='_get_type', string='Type')
    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle', required=True)
    driver_id = fields.Many2one('a4i.vehiclefleetmanager.driver', string='Driver')
    accident_date = fields.Date(string='Accident date')
    accident_location = fields.Char(string='Accident location')
    declaration_date = fields.Date(string='Declaration date', default=lambda self: fields.Datetime.now())
    internal_note = fields.Text(string='Internal notes')

    @api.multi
    def create_accident(self):

        accident_ids = []
        for wiz_rc in self:

            accident_vals = {'name': wiz_rc.name, 'vehicle_id': wiz_rc.vehicle_id.id, 'driver_id': wiz_rc.driver_id.id,
                             'accident_location': wiz_rc.accident_location, 'declaration_date': wiz_rc.declaration_date,
                             'accident_date': wiz_rc.accident_date, 'internal_note': wiz_rc.internal_note,
                             'type': wiz_rc.type}

            accident_rc = self.env['a4i.vehiclefleetmanager.vehicle.accident'].create(accident_vals)
            if accident_rc:
                accident_ids.append(accident_rc.id)
        if accident_ids:
            act_dict = self.env.ref('vehicle_fleet_manager.act_vehiclefleetmanager_accident_a4i').read()[0]
            act_dict['domain'] = [('id', 'in', accident_ids)]
            return act_dict
