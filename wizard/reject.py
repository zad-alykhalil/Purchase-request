from odoo import api, fields, models


class RejectWizard(models.TransientModel):
    _name = "reject.wizard"
    _description = "Rejection Reason"

    reject = fields.Text(string="Rejection Reason", required=True)

    def reject_action_button(self):
        get_reason = self.env['purchase.request'].browse(self.env.context.get('active_ids'))
        get_reason.reason = self.reject
        get_reason.state = 'reject'

    def back_action(self):
        return
