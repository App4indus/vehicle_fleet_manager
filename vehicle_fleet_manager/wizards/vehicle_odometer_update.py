# -*- coding: utf-8 -*-
import openerp
from openerp.exceptions import except_orm, ValidationError
from openerp import _, api, fields, models
from openerp.exceptions import AccessDenied, UserError, AccessError
from openerp.http import request


class A4I_vehiclefleetmanager_vehicle_odometer_update(models.TransientModel):
    """
        Wizard to update vehicle odometer
    """
    _name = 'a4i.vehiclefleetmanager.vehicle.odometer.update'
    _description = "Manually update vehicle odometer"

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle')
    odometer_value = fields.Integer(string='Odometer value')

    @api.multi
    def update_odometer(self):
        for wiz_rc in self:
            if self.vehicle_id:
                vals = {'vehicle_id': wiz_rc.vehicle_id.id, 'update_origin': "Manual update",
                        'odometer_value': wiz_rc.odometer_value, 'update_date': fields.datetime.now(),
                        'update_user_id': self.env.user.id}
                self.env['a4i.vehiclefleetmanager.vehicle.odometer'].create(vals)

            else:
                raise ValidationError(_("You must specify a vehicle"))
