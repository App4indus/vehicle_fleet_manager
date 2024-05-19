# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class A4I_vehicle_fleet_manager_label(models.Model):
    _inherit = 'a4i.administrative.contract'
    _description = 'Vehicle contracts'
    
    """
    Vehicle contracts linked to the vehicle
    """

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle', ondelete='restrict')
