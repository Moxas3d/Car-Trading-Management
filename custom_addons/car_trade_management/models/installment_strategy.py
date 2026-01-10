from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InstallmentStrategy(models.Model):
    _name = "car.trading.installment.strategy"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Installment Strategy"

    name = fields.Char(tracking=True)

    months = fields.Integer(
        required=True,
        help="Number of installment months (e.g. 6, 12, 24)",
        tracking=True,
    )

    bank_id = fields.Many2one("car.trading.bank", tracking=True)

    down_payment_percent = fields.Float(
        string="Down Payment %",
        help="Percentage of car price paid upfront",
        tracking=True,
    )

    bank_interest_rate = fields.Float(
        related="bank_id.interest_rate",
        string="Bank Interest Rate %",
        help="Total interest taken by bank",
        readonly=True,
    )

    company_funding_amount = fields.Float(
        string="Company Funding",
        help="Interest amount covered by company",
        tracking=True,
    )

    is_funded = fields.Boolean(
        string="Company Funded", compute="_compute_is_funded", store=True
    )

    active = fields.Boolean(default=True, tracking=True)

    bank_count = fields.Integer(compute="_compute_bank_count")

    def _compute_bank_count(self):
        for record in self:
            record.bank_count = 1 if record.bank_id else 0

    def action_open_bank(self):
        return {
            "name": "Bank",
            "type": "ir.actions.act_window",
            "res_model": "car.trading.bank",
            "view_mode": "form",
            "res_id": self.bank_id.id,
            "target": "current",
        }

    @api.constrains("months", "down_payment_percent", "company_funding_amount")
    def _check_validations(self):
        for record in self:
            if record.months <= 0:
                raise ValidationError("Months must be greater than 0.")
            if record.down_payment_percent < 0:
                raise ValidationError("Down Payment % cannot be negative.")
            if record.company_funding_amount < 0:
                raise ValidationError("Company Funding cannot be negative.")

    @api.depends("company_funding_amount")
    def _compute_is_funded(self):
        for rec in self:
            rec.is_funded = rec.company_funding_amount > 0
