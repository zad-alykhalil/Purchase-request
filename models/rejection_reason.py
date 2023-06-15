import datetime
from odoo import api, fields, models


class purchase_reject(models.Model):
    _name = 'rejection.reason'
    _description = 'Purchase Request'

    name = fields.Char('Name', required=False, )
