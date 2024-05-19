# -*- coding: utf-8 -*-
import openerp
from openerp.exceptions import except_orm, ValidationError
from openerp import _, api, fields, models
from openerp.exceptions import AccessDenied, UserError, AccessError
from openerp.http import request


class A4I_vehiclefleetmanager_fine_quick_add(models.TransientModel):
    """
        Wizard create fine quickly
    """
    _name = 'a4i.vehiclefleetmanager.fine.quick.create.wizard'
    _description = "Fine - quick creation"

    @api.onchange('citation_date', 'citation_location')
    def onchange_compute_name(self):
        name = ''
        if self.citation_location:
            name += '%s' % (self.citation_location)

        if self.citation_date:
            name += ', on %s' % (self.citation_date)

        self.name = name

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', required=True)
    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle', required=True)
    driver_id = fields.Many2one('a4i.vehiclefleetmanager.driver', string='Driver')
    citation_date = fields.Date(string='Fine date', help='Date of the fine', required=True)
    citation_location = fields.Char(string='Fine location', help='Location of the fine')
    internal_note = fields.Text(string='Internal notes')

    @api.multi
    def create_fine(self):

        fine_ids = []
        for wiz_rc in self:

            fine_vals = {'name': wiz_rc.name, 'vehicle_id': wiz_rc.vehicle_id.id, 'driver_id': wiz_rc.driver_id.id,
                         'citation_date': wiz_rc.citation_date, 'citation_location': wiz_rc.citation_location}

            fine_rc = self.env['a4i.vehiclefleetmanager.vehicle.fine'].create(fine_vals)
            if fine_rc:
                fine_ids.append(fine_rc.id)
        if fine_ids:
            act_dict = self.env.ref('vehicle_fleet_manager.act_vehiclefleetmanager_fine_a4i').read()[0]
            act_dict['domain'] = [('id', 'in', fine_ids)]
            return act_dict
