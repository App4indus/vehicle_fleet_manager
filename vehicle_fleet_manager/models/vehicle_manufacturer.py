# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, except_orm
import logging
import os
import base64

LOG = logging.getLogger("dicttoxml")


class A4I_vehicle_fleet_manager_vehicle_manufacturer(models.Model):
    _name = 'a4i.vehiclefleetmanager.vehicle.manufacturer'
    _description = 'Vehicle manufacturers'

    """
    Vehicle manufacturers
    """
    

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', help='Manufacturer name')
    code = fields.Char(string='Code', help='Manufacturer code')
    logo = fields.Binary(string='Logo',  help='Manufacturer logo')

    # ===========================================================================
    # METHODS
    # ===========================================================================

    @api.model
    def post_picture(self):
        """
        Import the manufacturer logo
        """
        manufacturer_rcs = self.search([])

        for manufacturer_rc in manufacturer_rcs:
            parent_dir = os.path.dirname(os.path.dirname(__file__))

            image_path = parent_dir+'/data/vehicle_manufacturer_logos/{code}.png'.format(code=manufacturer_rc.code)
            try:
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()

                if image_data:
                    manufacturer_rc.logo = base64.b64encode(image_data)
            except Exception as error:
                LOG.debug("Error during image import : ", str(error))
