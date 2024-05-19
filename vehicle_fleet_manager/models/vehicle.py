# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import ValidationError, except_orm
from datetime import datetime, timedelta
import logging

LOG = logging.getLogger("dicttoxml")


class A4I_vehiclefleetmanager_vehicle(models.Model):
    _name = 'a4i.vehiclefleetmanager.vehicle'
    _description = 'Vehicles'
    
    """
    Vehicles
    """

    # State selection
    @api.model
    def _get_state(self):
        """
        Return the state selection
        """
        return [('requested', _('Requested')), ('ordered', _('Ordered')), ('in_service', _('In service')), ('out_service', _('Out service'))]

    # Acquisition selection
    @api.model
    def _get_acquisition(self):
        """
        Return the acquisition selection
        """
        return [('purchase', _('Purchase')), ('lld', _('Long-Term Lease')), ('lcd', _('Song-Term Rental')),
                ('loa', _('Lease with Option to Buy')), ('leasing', _('Finance Lease')), ('other', _('Other'))]

    # Transmission selection
    @api.model
    def _get_transmission_type(self):
        """
        Return the transmission selection
        """
        return [('manual', _('Manual')), ('sequential', _('Sequential')), ('automatic', _('Automatic')), ('other', _('Other'))]

    # Energy selection
    @api.model
    def _get_energy_type(self):
        """
        Return the energy selection
        """
        return [('gasoline', _('Gasoline')), ('diesel', _('Diesel')), ('electric', _('Electric')),
                ('hybrid', _('hybrid')), ('plugin_hybrid', _('Plug-in hybrid')), ('other', _('Other'))]

    # Compute odometer last value
    @api.one
    @api.depends('odometer_ids')
    def _compute_last_odometer_value(self):
        """
        Compute the last odometer value
        :return: int
        """
        value = 0
        odometer_rc = self.odometer_ids.search([('vehicle_id', '=', self.id)], limit=1, order='odometer_value desc')
        if odometer_rc:
            value = odometer_rc.odometer_value
        self.last_odometer_value = value

    # Compute total costs
    @api.one
    @api.depends('accident_ids', 'fine_ids', 'contract_ids')
    def _compute_total_costs(self):
        """
        Compute the total costs
        :return: float
        """
        for vehicle in self:
            contract_total_cost = sum(cost.total_cost for cost in vehicle.contract_ids if cost.total_cost) or 0
            fine_total_cost = sum(cost.amount for cost in vehicle.fine_ids if cost.amount) or 0
            accident_total_cost = sum(cost.reparation_amount for cost in vehicle.accident_ids if cost.reparation_amount) or 0
            purchase_cost = vehicle.purchase_cost or 0

            vehicle.total_cost = contract_total_cost + fine_total_cost + accident_total_cost + purchase_cost

    @api.one
    @api.depends('lat', 'lng')
    def _compute_is_located(self):
        """
        Compute the is located field
        :return: bool
        """
        if self.lat != 0.0 and self.lng != 0.0:
            self.is_located = True
        else:
            self.is_located = False

    # ===========================================================================
    # ONCHANGES
    # ===========================================================================
    @api.onchange('model_id')
    def _onchange_propagate_model(self):
        """
        Propagate the model's infos
        :return: None
        """
        fields = ['vehicle_manufacturer_id', 'image', 'model_year', 'seats_nb', 'doors_nb', 'transmission_type',
                  'energy_type', 'fiscal_horsepower', 'engine_power', 'co2_emissions', 'environmental_bonus_malus',
                  'type_id']
        model = self.model_id
        for field in fields:
            val = getattr(model, field)
            setattr(self, field, val)

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    state = fields.Selection(selection='_get_state', string='State', default='requested')
    name = fields.Char(string='Name', required=True)
    acquisition_mode = fields.Selection(selection='_get_acquisition', string='Acquisition mode')
    responsible_id = fields.Many2one('res.users', string='Responsible', help='Responsible of the vehicle', ondelete='restrict')
    type_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle.type', string='Type', required=True, ondelete='set null')
    model_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle.model', string='Model', help="Set the model and all model's infos will be propagated to the vehicle", ondelete='set null')
    vehicle_manufacturer_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle.manufacturer', string='Manufacturer', required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', help='Partner who sell the vehicle', domain="[('is_supplier', '=', True)]")
    image = fields.Binary(string='Logo',  help='Image')
    registration_date = fields.Date(string='Registration date', help='registration date of the vehicle')
    expected_delivery_date = fields.Date(string='Expected delivery date', help='Expected delivery date of the vehicle')
    numberplate = fields.Char(string='Numberplate', help='Numberplate of the vehicle')
    chassis_number = fields.Char(string='Chassis number', help='Chassis number of the vehicle')
    model_year = fields.Char(string='Model year', help='Model year of the vehicle')
    last_odometer_value = fields.Integer(compute='_compute_last_odometer_value', string='Last Odometer', help='odometer of the vehicle')
    internal_note = fields.Text(string='Internal notes')
    tag_ids = fields.Many2many('a4i.vehiclefleetmanager.label', 'a4i_vehiclefleetmanager_vehicle_tag_rel', 'tag_id', 'vehicle_id', string='Tags')
    seats_nb = fields.Integer(string='Seats nb')
    doors_nb = fields.Integer(string='Doors nb')
    color = fields.Char(string='Color')
    transmission_type = fields.Selection(selection='_get_transmission_type', string='Transmission')
    energy_type = fields.Selection(selection='_get_energy_type', string='Energy')
    fiscal_horsepower = fields.Integer(string='Fiscal horsepower')
    engine_power = fields.Integer(string='Engine power (cv)')
    co2_emissions = fields.Integer(string='CO2 emissions (g/kms)')
    environmental_bonus_malus = fields.Integer(string='Environmental bonus / malus')
    location = fields.Char(string='Location')
    assignation_date = fields.Date(string='Assignation date')
    assigned_driver_id = fields.Many2one('a4i.vehiclefleetmanager.driver', string='Assigned driver', help='Driver assigned to the vehicle', ondelete='restrict')
    contract_ids = fields.One2many('a4i.administrative.contract', 'vehicle_id', string='Contracts', ondelete='set null')
    intervention_ids = fields.One2many('a4i.vehiclefleetmanager.vehicle.intervention', 'vehicle_id', string='Interventions', ondelete='restrict')
    odometer_ids = fields.One2many('a4i.vehiclefleetmanager.vehicle.odometer', 'vehicle_id', string='Odometers', ondelete='restrict')
    fine_ids = fields.One2many('a4i.vehiclefleetmanager.vehicle.fine', 'vehicle_id', string='Fines', ondelete='set null')
    accident_ids = fields.One2many('a4i.vehiclefleetmanager.vehicle.accident', 'vehicle_id', string='Accidents', ondelete='restrict')
    use_ids = fields.One2many('a4i.vehiclefleetmanager.vehicle.use', 'vehicle_id', string='Uses', ondelete='restrict')
    document_ids = fields.Many2many('document.openprod', 'a4i_vehiclefleetmanager_vehicle_doc_rel', string='Documents', ondelete='set null')
    purchase_cost = fields.Float(string='Purchase cost', help='Cost (if purchased)', default=0)
    total_cost = fields.Float(string='Total cost', compute='_compute_total_costs')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, ondelete='restrict',
                                  default=lambda self: self.env.user.company_id.currency_id)

    # Map
    """
    Geolocation fields
    #TODO? : Add a cron to update the geolocation
    #TODO? : Add API services to get the geolocation
    """
    geolocation_enabled = fields.Boolean(string='Geolocation enabled')
    geolocation_reference = fields.Char(string='Geolocation reference')
    last_geoloc_datetime = fields.Datetime(string='Last geolocation', help='Last geolocation')
    lat = fields.Float(string='Latitude', default=0.0, digits=dp.get_precision('Coordinates'), required=False)
    lng = fields.Float(string='Longitude', default=0.0, digits=dp.get_precision('Coordinates'), required=False)
    readed_by_api = fields.Boolean(string='Readed by the api', default=False, required=False)
    is_located = fields.Boolean(string='Is located', compute='_compute_is_located', required=False)

    # ===========================================================================
    # METHODS
    # ===========================================================================

    @api.multi
    def wkf_draft(self):
        """
        Set the vehicle as draft
        """
        for vehicle_rc in self:
            vehicle_rc.write({'state': 'draft'})

    @api.multi
    def wkf_requested(self):
        """
        Set the vehicle as requested
        """
        for vehicle_rc in self:
            vehicle_rc.write({'state': 'requested'})

    @api.multi
    def wkf_ordered(self):
        """
        Set the vehicle as ordered
        """
        for vehicle_rc in self:
            vehicle_rc.write({'state': 'ordered'})

    @api.multi
    def wkf_in_service(self):
        """ 
        Set the vehicle as in service
        """
        for vehicle_rc in self:
            vehicle_rc.write({'state': 'in_service'})

    @api.multi
    def wkf_out_service(self):
        """
        Set the vehicle as out service
        """
        for vehicle_rc in self:
            vehicle_rc.write({'state': 'out_service'})

    @api.multi
    def show_contracts(self):
        """
        Show the contracts
        :return: dict
        """
        act_dict = self.env.ref('vehicle_fleet_manager.act_vehiclefleetmanager_contract_a4i').read()[0]
        act_dict['domain'] = [('vehicle_id', '=', self.id)]
        return act_dict

    @api.multi
    def show_fines(self):
        """
        Show the fines
        :return: dict
        """
        act_dict = self.env.ref('vehicle_fleet_manager.act_vehiclefleetmanager_fine_a4i').read()[0]
        act_dict['domain'] = [('vehicle_id', '=', self.id)]
        return act_dict

    @api.multi
    def show_uses(self):
        """
        Show the uses
        :return: dict
        """
        act_dict = self.env.ref('vehicle_fleet_manager.act_vehiclefleetmanager_use_a4i').read()[0]
        act_dict['domain'] = [('vehicle_id', '=', self.id)]
        return act_dict

    @api.multi
    def show_interventions(self):
        """
        Show the interventions
        :return: dict
        """
        act_dict = self.env.ref('vehicle_fleet_manager.act_vehiclefleetmanager_intervention_a4i').read()[0]
        act_dict['domain'] = [('vehicle_id', '=', self.id)]
        return act_dict

    @api.multi
    def show_accidents(self):
        """
        Show the accidents
        :return: dict
        """
        act_dict = self.env.ref('vehicle_fleet_manager.act_vehiclefleetmanager_accident_a4i').read()[0]
        act_dict['domain'] = [('vehicle_id', '=', self.id)]
        return act_dict

    @api.multi
    def update_odometer(self):
        """
        Update the odometer
        :return: dict
        """
        wiz_obj = self.env['a4i.vehiclefleetmanager.vehicle.odometer.update']

        for vehicle_rc in self:

            vals_wiz = {'vehicle_id': vehicle_rc.id}
            wiz_rc = wiz_obj.create(vals_wiz)
            return {
                'name': _('Update vehicle odometer'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'a4i.vehiclefleetmanager.vehicle.odometer.update',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': wiz_rc.id,
                'nodestroy': True,
            }

    @api.multi
    def create_intervention(self):
        """
        Create an intervention
        :return: dict
        """

        for vehicle_rc in self:

            return {
                'name': _('Create intervention'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'a4i.vehiclefleetmanager.vehicle.intervention',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {'default_vehicle_id': vehicle_rc.id},
                'nodestroy': True,
            }

    @api.multi
    def create_accident(self):
        """
        Create an accident
        :return: dict
        """

        for vehicle_rc in self:

            return {
                'name': _('Create accident'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'a4i.vehiclefleetmanager.vehicle.accident',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {'default_vehicle_id': vehicle_rc.id},
                'nodestroy': True,
            }

    @api.multi
    def request_use(self):
        """
        Request a use
        :return: dict
        """

        wiz_obj = self.env['a4i.vehiclefleetmanager.vehicle.request.use.wizard']

        for vehicle_rc in self:
            vals_wiz = {'vehicle_id': vehicle_rc.id}
            wiz_rc = wiz_obj.create(vals_wiz)
            return {
                'name': _('Use request'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'a4i.vehiclefleetmanager.vehicle.request.use.wizard',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': wiz_rc.id,
                'nodestroy': True,
            }

    @api.multi
    def get_address_values(self):
        """
        Get the address values
        """

        return True

    # ===========================================================================
    # CRONS
    # ===========================================================================


class A4I_vehiclefleetmanager_vehicle_type(models.Model):
    _name = 'a4i.vehiclefleetmanager.vehicle.type'
    _description = 'Vehicle types'

    """
    Vehicle types
    """

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name')


class A4I_vehiclefleetmanager_vehicle_model(models.Model):
    _name = 'a4i.vehiclefleetmanager.vehicle.model'
    _description = 'Vehicle models'

    """
    Vehicle model
    """

    # Transmission selection
    @api.model
    def _get_transmission_type(self):
        """
        Return the transmission selection
        :return: list
        """
        return [('manual', _('Manual')), ('sequential', _('Sequential')), ('automatic', _('Automatic')),
                ('other', _('Other'))]

    # Energy selection
    @api.model
    def _get_energy_type(self):
        """
        Return the energy selection
        :return: list
        """ 
        return [('gasoline', _('Gasoline')), ('diesel', _('Diesel')), ('electric', _('Electric')),
                ('hybrid', _('hybrid')), ('plugin_hybrid', _('Plug-in hybrid')), ('other', _('Other'))]

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', required=True)
    type_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle.type', string='Type', required=True, ondelete='set null')
    vehicle_manufacturer_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle.manufacturer', string='Manufacturer', required=True, ondelete='restrict')
    image = fields.Binary(string='Logo', help='Image')
    model_year = fields.Char(string='Model year', help='Model year of the vehicle')
    seats_nb = fields.Integer(string='Seats nb')
    doors_nb = fields.Integer(string='Doors nb')
    transmission_type = fields.Selection(selection='_get_transmission_type', string='Transmission')
    energy_type = fields.Selection(selection='_get_energy_type', string='Energy')
    fiscal_horsepower = fields.Integer(string='Fiscal horsepower')
    engine_power = fields.Integer(string='Engine power (cv)')
    co2_emissions = fields.Integer(string='CO2 emissions (g/kms)')
    environmental_bonus_malus = fields.Integer(string='Environmental bonus / malus')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, ondelete='restrict',
                                  default=lambda self: self.env.user.company_id.currency_id)
