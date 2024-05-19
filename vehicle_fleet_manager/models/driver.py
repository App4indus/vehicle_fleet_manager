# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class A4I_vehiclefleetmanager_driver(models.Model):
    _name = 'a4i.vehiclefleetmanager.driver'
    _description = 'Vehicle drivers'
    
    """
    Drivers of the vehicle
    """


    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', required=True)
    first_name = fields.Char(string='First name', required=True)
    driving_license_date = fields.Date(string='Driving license date')
    driving_license_document = fields.Many2one('document.openprod', string='Driving license document')
