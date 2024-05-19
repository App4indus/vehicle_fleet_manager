# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, except_orm


class A4I_vehiclefleetmanager_vehicle_fine(models.Model):
    _name = 'a4i.vehiclefleetmanager.vehicle.fine'
    _description = 'Vehicle fines'
    
    """
    Vehicle fine
    """

    # State selection
    @api.model
    def _get_state(self):
        """
        Return the list of states
        :return: list
        """
        return [('received', _('Received')), ('pending_payment', _('Pending payment')),
                ('paid', _('Paid')), ('contested', _('Contested'))]

    @api.model
    def _get_months(self):
        """
        Return the list of months
        :return: list
        """
        return [
            ('01', _('January')),
            ('02', _('February')),
            ('03', _('March')),
            ('04', _('April')),
            ('05', _('May')),
            ('06', _('June')),
            ('07', _('July')),
            ('08', _('August')),
            ('09', _('September')),
            ('10', _('October')),
            ('11', _('November')),
            ('12', _('December'))
        ]

    @api.one
    @api.depends('citation_date')
    def _compute_date(self):
        """
        Compute the date
        :return: bool
        """
        date = False
        # On prend la date réelle
        if self.citation_date:
            date = fields.Date.from_string(self.citation_date)

        else:
            self.month = False
            self.year = False

        if date:
            # On récupère le nom du jour et le numéro de l'année
            isocal = date.isocalendar()
            self.day = str(isocal[2])
            self.year = str(isocal[0])

            # On récupère le mois
            if len(str(date.month)) == 1:
                self.month = '0%s' % (str(date.month))
            else:
                self.month = str(date.month)

    # ===========================================================================
    # COLUMNS
    # ===========================================================================

    name = fields.Char(string='Name', required=True)
    state = fields.Selection(selection='_get_state', string='State', default='received')
    vehicle_id = fields.Many2one('a4i.vehiclefleetmanager.vehicle', string='Vehicle', ondelete='restrict')
    driver_id = fields.Many2one('a4i.vehiclefleetmanager.driver', string='Driver', ondelete='restrict')
    citation_date = fields.Date(string='Citation date')
    citation_location = fields.Char(string='Citation location')
    contestation_date = fields.Date(string='Contestation date')
    amount = fields.Float(string='Fine amount')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, ondelete='restrict', default=lambda self: self.env.user.company_id.currency_id)
    document_ids = fields.Many2many('document.openprod', 'a4i_vehiclefleetmanager_vehicle_fine_rel', string='Documents')
    internal_note = fields.Text(string='Internal notes')

    # Date
    month = fields.Selection(selection='_get_months', string='Month', compute='_compute_date', store=True)
    year = fields.Char(string='Year', size=4, compute='_compute_date', store=True)

    # ===========================================================================
    # METHODS
    # ===========================================================================

    @api.multi
    def wkf_received(self):
        """
        Set the fine as received
        """
        for fine_rc in self:
            fine_rc.write({'state': 'received'})

    @api.multi
    def wkf_pending_payment(self):
        """
        Set the fine as pending payment
        """
        for fine_rc in self:
            fine_rc.write({'state': 'pending_payment'})

    @api.multi
    def wkf_paid(self):
        """
        Set the fine as paid
        """
        for fine_rc in self:
            fine_rc.write({'state': 'paid'})

    @api.multi
    def wkf_contest(self):
        """
        Set the fine as contested
        """
        for fine_rc in self:
            fine_rc.write({'state': 'contested'})
