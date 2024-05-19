# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, except_orm
from datetime import datetime, timedelta
import logging

LOG = logging.getLogger("dicttoxml")


class A4I_vehicle_fleet_manager_vehicle_use(models.Model):
    _name = 'a4i.vehiclefleetmanager.vehicle.use'
    _description = 'Vehicle uses'

    """
    Vehicle uses
    """

    # State selection
    @api.model
    def _get_state(self):
        """
        Get state
        :return: state
        """
        return [('requested', _('Requested')), ('accepted', _('Accepted')), ('rejected', _('Rejected')), ('done', _('Done')), ('cancel', _('Cancel'))]

    @api.model
    def create(self, vals):
        """
        Override the create method to update the odometer
        :param vals: dict
        :return: recordset
        """
        rc = super(A4I_vehicle_fleet_manager_vehicle_use, self).create(vals=vals)

        # Update odometer
        if rc.vehicle_id and rc.state == 'done' and rc.odometer:
            vals = {'vehicle_id': rc.vehicle_id.id, 'update_origin': "Use",
                    'odometer_value': rc.odometer, 'update_date': fields.datetime.now(),
                    'update_user_id': self.env.user.id}
            self.env['a4i.vehiclefleetmanager.vehicle.odometer'].create(vals)

        return rc

    @api.one
    @api.depends('start_date', 'start_date', 'vehicle_id')
    def _compute_name(self):
        """
        Compute the name
        :return: str
        """
        if self.vehicle_id:
            self.name = '{vehicle_name} from {start} to {end}'.format(vehicle_name=self.vehicle_id.name,
                                                                      start=self.start_date or '', end=self.end_date or '')

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', help='Name', compute='_compute_name')
    state = fields.Selection(selection='_get_state', string='State', default='requested')
    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle', help='Vehicle used')
    request_creation_date = fields.Date(string='Request date', help='Date of request', default=lambda *self: fields.Date.today())
    start_date = fields.Date(string='Start date', help='Start date of the use')
    end_date = fields.Date(string='End date', help='End date of the use')
    driver_id = fields.Many2one('a4i.vehiclefleetmanager.driver', string='Driver')
    notes = fields.Text(string='Comments')

    # ===========================================================================
    # METHODS
    # ===========================================================================

    @api.multi
    def wkf_accept(self):
        """
        Set the use as accepted
        """
        for use_rc in self:
            use_rc.state = 'accepted'

    @api.multi
    def wkf_reject(self):
        """
        Set the use as rejected
        """
        for use_rc in self:
            use_rc.state = 'rejected'

    @api.multi
    def wkf_done(self):
        """
        Set the use as done
        """
        for use_rc in self:
            use_rc.state = 'done'

    @api.multi
    def wkf_cancel(self):
        """
        Set the use as cancel
        """
        for use_rc in self:
            use_rc.state = 'cancel'
