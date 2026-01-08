from odoo import models, fields, api


class Bank(models.Model):
    _name = "car.trading.bank"
    _description = "Financing Bank"

    name = fields.Char()

    interest_rate = fields.Float(
        string="Interest Rate (%)",
        required=True,
        digits=(4, 2),
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
