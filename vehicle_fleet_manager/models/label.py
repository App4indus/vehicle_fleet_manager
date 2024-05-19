# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, except_orm
from datetime import datetime, timedelta
import logging

LOG = logging.getLogger("dicttoxml")


class A4I_vehicle_fleet_manager_label(models.Model):
    _name = 'a4i.vehiclefleetmanager.label'
    _description = 'Vehicle labels'
    
    """
    Vehicles labels
    """


    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name')
    color = fields.Integer(string='Color')
