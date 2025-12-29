from odoo import models, fields


class PaymentStrategy(models.Model):
    _name = "car.trading.payment.strategy"
    _description = "Payment Strategy"

    name = fields.Char(required=True)

    months = fields.Integer(
        required=True, help="Number of installment months (e.g. 6, 12, 24)"
    )

    down_payment_percent = fields.Float(
        string="Down Payment %", help="Percentage of car price paid upfront"
    )

    bank_interest_amount = fields.Float(
        string="Bank Interest Amount", help="Total interest taken by bank"
    )

    company_funding_amount = fields.Float(
        string="Company Funding", help="Interest amount covered by company"
    )

    is_funded = fields.Boolean(
        string="Company Funded", compute="_compute_is_funded", store=True
    )

    active = fields.Boolean(default=True)
