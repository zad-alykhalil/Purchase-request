import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'

    name = fields.Char(string="Request Name", required=True)
    partner_id = fields.Many2one('res.partner', string="Vendor", required=True, )
    purchase_number = fields.Char("Request Number", readonly=True, required=True, copy=False, default='New')
    user_id = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.user,
                              states={'approve': [('readonly', True)], 'reject': [('readonly', True)],
                                      'cancel': [('readonly', True)]}, )
    date_start = fields.Date(string="Start Date", default=datetime.date.today(),
                             states={'approve': [('readonly', True)], 'reject': [('readonly', True)],
                                     'cancel': [('readonly', True)]}, )
    date_end = fields.Date(string="End date", required=True,
                           states={'approve': [('readonly', True)], 'reject': [('readonly', True)],
                                   'cancel': [('readonly', True)]}, )
    reason = fields.Many2many('rejection.reason', string="Rejection Reason", readonly=True, )
    order_line_ids = fields.One2many('purchase.request.line', 'request_id', string="Order Line", required=True,
                                     states={'approve': [('readonly', True)], 'reject': [('readonly', True)],
                                             'cancel': [('readonly', True)]}, )
    sum_total = fields.Float(string="Total", compute='_compute_sum_total', readonly=True,
                             states={'approve': [('readonly', True)], 'reject': [('readonly', True)],
                                     'cancel': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Draft'),
         ('to_be_approved', 'To Be Approved'),
         ('approve', 'Approve'),
         ('reject', 'Reject'),
         ('cancel', 'Cancel')], string="State", default='draft')

    purchase_order_count = fields.Integer(compute="_compute_purchase_order", )

    def _compute_purchase_order(self):
        for rec in self:
            order_count = self.env['purchase.order'].search_count([('origin', '=', rec.name)])
            rec.purchase_order_count = order_count

    def my_smart_button_action(self):
        # define the action to be performed when the smart button is clicked
        # this could involve querying related data or performing a specific action
        domain = [('origin', '=', self.name)]
        return {
            'name': 'Purchase Orders',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'purchase.order',
            'domain': domain,
        }

    @api.onchange('date_end')
    def _check_validity_date(self):
        for record in self:
            if record.date_end and record.date_start:
                if record.date_end < record.date_start:
                    raise ValidationError("End date should not be before start date!")

    @api.depends('order_line_ids')
    def _compute_sum_total(self):
        for record in self:
            sum_var = 0
            for line in record.order_line_ids:
                sum_var += line.total
            record.sum_total = sum_var

    @api.model
    def create(self, vals):
        if vals.get('purchase_number', 'New') == 'New':
            vals['purchase_number'] = self.env['ir.sequence'].next_by_code(
                'purchase.request.sequence') or 'New'
        result = super(PurchaseRequest, self).create(vals)
        return result

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

    def action_po(self):
        for record in self:
            order_values = {
                'origin': self.name,
                'partner_id': self.partner_id.id,
                'user_id': record.user_id.id,
                'date_order': record.date_start,
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'product_qty': line.quantity,
                    'price_unit': line.cost_price,
                }) for line in self.order_line_ids]

            }
            purchase_order = self.env['purchase.order'].create(order_values)
            return {
                'name': 'Purchase Order Created',
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'res_id': purchase_order.id,
            }


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
