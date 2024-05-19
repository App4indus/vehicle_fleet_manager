# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, except_orm


class A4I_vehiclefleetmanager_vehicle_odometer(models.Model):
    _name = 'a4i.vehiclefleetmanager.vehicle.odometer'
    _description = 'Vehicle odometers'
    
    """
    Vehicle odometers
    """

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle')
    odometer_value = fields.Integer(string='Odometer value', help='Odometer value')
    update_date = fields.Datetime(string='Update date')
    update_user_id = fields.Many2one('res.users', string='Update by')
    update_origin = fields.Char(string='Update origin')
    internal_note = fields.Text(string='Internal notes')

