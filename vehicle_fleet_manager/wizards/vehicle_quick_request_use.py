# -*- coding: utf-8 -*-
import openerp
from openerp.exceptions import except_orm, ValidationError
from openerp import _, api, fields, models
from openerp.exceptions import AccessDenied, UserError, AccessError
from openerp.http import request


class A4I_vehiclefleetmanager_vehicle_request_use_wizard(models.TransientModel):
    """
        Wizard to request use of vehicle
    """
    _name = 'a4i.vehiclefleetmanager.vehicle.request.use.wizard'
    _description = "Request a vehicle use"

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle', required=True)
    driver_id = fields.Many2one('a4i.vehiclefleetmanager.driver', string='Driver')
    start_date = fields.Date(string='Start date')
    end_date = fields.Date(string='End date')
    notes = fields.Text(string='Comments')

    # ===========================================================================
    # METHODS
    # ===========================================================================

    @api.multi
    def create_request(self):

        use_vals = {'state': 'requested', 'request_creation_date': fields.Date.today(), 'driver_id': self.driver_id.id,
                    'vehicle_id': self.vehicle_id.id, 'start_date': self.start_date, 'end_date': self.end_date,
                    'notes': self.notes}

        use_rc = self.env['a4i.vehiclefleetmanager.vehicle.use'].create(use_vals)
        if use_rc:
            act_dict = self.env.ref('vehicle_fleet_manager.act_vehiclefleetmanager_use_a4i').read()[0]
            act_dict['domain'] = [('id', '=', use_rc.id)]
            return act_dict
