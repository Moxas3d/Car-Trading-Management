from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Bank(models.Model):
    _name = "car.trading.bank"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Financing Bank"

    name = fields.Char()

    interest_rate = fields.Float(
        string="Interest Rate (%)",
        required=True,
        digits=(4, 2),
        tracking=True,
    )

    max_installment_months = fields.Integer(
        string="Max Installment Months",
        default=24,
    )

    notes = fields.Text()

    _sql_constraints = [
        (
            "check_interest_rate_positive",
            "CHECK(interest_rate >= 0)",
            "The interest rate must be a positive value!",
        )
    ]

    @api.constrains("max_installment_months")
    def _check_max_installment_months(self):
        for record in self:
            if record.interest_rate < 0:
                raise ValidationError("The interest rate must be a positive value!")
            if record.max_installment_months <= 0:
                raise ValidationError("Max Installment Months must be greater than 0.")

    def property_xlsx_report(self):
        return {
            "type": "ir.actions.act_url",
            "url": f"/excel/report/car.trading.bank/{self.env.context.get('active_ids')}",
            "target": "new",
        }
