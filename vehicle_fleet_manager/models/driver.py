# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class A4I_vehiclefleetmanager_driver(models.Model):
    _name = 'a4i.vehiclefleetmanager.driver'
    _description = 'Vehicle drivers'
    
    """
    Drivers of the vehicle
    """

    @api.one
    @api.depends('last_name', 'first_name')
    def _compute_name(self):
        """ Compute name """
        if self.is_user and self.user_id:
            self.name = self.user_id.name
        elif self.first_name and self.last_name:
            self.name = self.first_name + self.last_name

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', compute='_compute_name')
    is_user = fields.Boolean(string='Is registered user', default=False)
    user_id = fields.Many2one('res.users', string='User')
    last_name = fields.Char(string='Last name')
    first_name = fields.Char(string='First name')
    driving_license_date = fields.Date(string='Driving license date')
    driving_license_document = fields.Many2one('document.openprod', string='Driving license document')
