import datetime
from odoo import api, fields, models


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'

    name = fields.Many2one('res.users', string="Name", default=lambda self: self.env['res.users'].search([]),
                           states={'approve': [('readonly', True)], 'reject': [('readonly', True)], 'cancel': [('readonly', True)]}, )

    start_date = fields.Date(string="Start Date", default=datetime.date.today(),
                             states={'approve': [('readonly', True)], 'reject': [('readonly', True)], 'cancel': [('readonly', True)]}, )
    end_date = fields.Date(string="End_date", required=True,
                           states={'approve': [('readonly', True)], 'reject': [('readonly', True)], 'cancel': [('readonly', True)]}, )
    reason = fields.Text(string="Rejection Reason", readonly=True, )
    order_line = fields.One2many('purchase.request.line', 'request_id', string="Order Line", required=True,
                                 states={'approve': [('readonly', True)], 'reject': [('readonly', True)], 'cancel': [('readonly', True)]}, )
    sum_total = fields.Float(string="Total", compute='_compute_sum_total', readonly=True,
                             states={'approve': [('readonly', True)], 'reject': [('readonly', True)], 'cancel': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Draft'),
         ('to_be_approved', 'To Be Approved'),
         ('approve', 'Approve'),
         ('reject', 'Reject'),
         ('cancel', 'Cancel')], string="State", default='draft')

    @api.depends('order_line')
    def _compute_sum_total(self):
        for record in self:
            sum_var = 0
            for line in record.order_line:
                sum_var += line.total
            record.sum_total = sum_var

    def draft(self):
        for record in self:
            record.state = 'draft'

    def to_be_approved(self):
        for record in self:
            record.state = 'to_be_approved'

    def approve(self):
        for record in self:
            record.state = 'approve'

    def cancelled(self):
        for record in self:
            record.state = 'cancel'


class PurchaseOrderLines(models.Model):
    _name = 'purchase.request.line'
    _description = 'Order Lines'

    request_id = fields.Many2one('purchase.request', string="ID", required=True, )
    product_id = fields.Many2one('product.product', string="Product ID", required=True, )
    description = fields.Char(related='product_id.name', string='Product Name', required=True, )
    quantity = fields.Float(string='Quantity', default=1, required=True, )
    cost_price = fields.Float(related='product_id.standard_price', string="Cost Price", required=True, )
    total = fields.Float(string="Total", required=True, compute='_compute_total', readonly=True, )

    @api.depends('quantity', 'cost_price')
    def _compute_total(self):
        for r in self:
            r.total = r.quantity * r.cost_price
