# -*- coding: utf-8 -*-
import openerp
from openerp.exceptions import except_orm, ValidationError
from openerp import _, api, fields, models
from openerp.exceptions import AccessDenied, UserError, AccessError
from openerp.http import request


class A4I_vehiclefleetmanager_vehicle_quick_add(models.TransientModel):
    """
        Wizard create vehicle quickly
    """
    _name = 'a4i.vehiclefleetmanager.vehicle.quick.create.wizard'
    _description = "Vehicle - quick creation"

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', required=True)
    vehicle_manufacturer_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle.manufacturer', string='Manufacturer', required=True)
    vehicle_model_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle.model', string='Model', help="Set the model and all model's infos will be propagated to the vehicle", ondelete='set null')
    responsible_id = fields.Many2one('res.users', string='Responsible', help='Responsible of the vehicle', required=True)
    type_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle.type', string='Type', required=True)
    registration_date = fields.Date(string='Registration date', help='registration date of the vehicle')
    numberplate = fields.Char(string='Numberplate', help='Numberplate of the vehicle')

    @api.multi
    def create_vehicle(self):

        vehicle_ids = []
        for wiz_rc in self:

            vehicle_vals = {'name': wiz_rc.name, 'vehicle_manufacturer_id': wiz_rc.vehicle_manufacturer_id.id,
                            'responsible_id': wiz_rc.responsible_id.id, 'type_id': wiz_rc.type_id.id,
                            'vehicle_model_id': wiz_rc.vehicle_model_id.id,
                            'registration_date': wiz_rc.registration_date, 'numberplate': wiz_rc.numberplate}

            vehicle_rc = self.env['a4i.vehiclefleetmanager.vehicle'].create(vehicle_vals)
            if vehicle_rc:
                vehicle_ids.append(vehicle_rc.id)
        if vehicle_ids:
            act_dict = self.env.ref('vehicle_fleet_manager.act_vehiclefleetmanager_vehicle_a4i').read()[0]
            act_dict['domain'] = [('id', 'in', vehicle_ids)]
            return act_dict
