from odoo import api, fields, models


class RejectWizard(models.TransientModel):
    _name = "reject.wizard"
    _description = "Rejection Reason"

    reject = fields.Many2one('rejection.reason', string="Rejection Reason", required=True)

    def reject_action_button(self):
        get_reason = self.env['purchase.request'].browse(self.env.context.get('active_ids'))
        get_reason.reason = self.rejecta
        get_reason.state = 'reject'
        send_reason = self.env['rejection.reason'].browse(self.env.context.get('active_ids'))
        get_reason.write({
            'reason': [(0, 0, [self.reject.id])]
        })

    def back_action(self):
        return
