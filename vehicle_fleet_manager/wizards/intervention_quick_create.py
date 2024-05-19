# -*- coding: utf-8 -*-
import openerp
from openerp.exceptions import except_orm, ValidationError
from openerp import _, api, fields, models
from openerp.exceptions import AccessDenied, UserError, AccessError
from openerp.http import request


class A4I_vehiclefleetmanager_intervention_quick_add(models.TransientModel):
    """
        Wizard create intervention quickly
    """
    _name = 'a4i.vehiclefleetmanager.intervention.quick.create.wizard'
    _description = "Intervention - quick creation"

    @api.onchange('type_id', 'supplier_id')
    def onchange_compute_name(self):
        name = ''
        if self.type_id:
            name += '%s' % (self.type_id.name)

        if self.planned_date:
            name += ' on %s' % (self.planned_date)

        self.name = name

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', required=True)
    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle', required=True)
    type_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle.intervention.type', string='Type', required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', help='Partner who maintened the vehicle',
                                  domain="[('is_supplier', '=', True)]")
    planned_date = fields.Date(string='Planned intervention date', required=True)
    internal_note = fields.Text(string='Internal notes')

    @api.multi
    def create_intervention(self):

        intervention_ids = []
        for wiz_rc in self:

            inter_vals = {'name': wiz_rc.name, 'vehicle_id': wiz_rc.vehicle_id.id, 'supplier_id': wiz_rc.supplier_id.id,
                         'planned_date': wiz_rc.planned_date, 'internal_note': wiz_rc.internal_note,
                         'type_id': wiz_rc.type_id.id}

            inter_rc = self.env['a4i.vehiclefleetmanager.vehicle.intervention'].create(inter_vals)
            if inter_rc:
                intervention_ids.append(inter_rc.id)
        if intervention_ids:
            act_dict = self.env.ref('vehicle_fleet_manager.act_vehiclefleetmanager_intervention_a4i').read()[0]
            act_dict['domain'] = [('id', 'in', intervention_ids)]
            return act_dict
