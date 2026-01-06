from odoo import models, fields, api

from datetime import date


class CarTradingInstallment(models.Model):
    _name = "car.trading.installment"
    _description = "Car Trading Installment"
    _order = "due_date"

    sale_id = fields.Many2one(
        "car.trading.sale.order", string="Sale Order", ondelete="cascade"
    )

    partner_id = fields.Many2one(related="sale_id.customer_id", store=True)

    bank_id = fields.Many2one(
        related="sale_id.installment_strategy_id.bank_id", store=True
    )

    sequence = fields.Integer(required=True)
    amount = fields.Float(required=True)
    due_date = fields.Date(required=True)
    paid = fields.Boolean(default=False)

    state = fields.Selection(
        [("due", "Due"), ("overdue", "Overdue"), ("paid", "Paid")],
        compute="_compute_state",
        store=True,
    )

    @api.depends("paid", "due_date")
    def _compute_state(self):
        today = date.today()
        for rec in self:
            if rec.paid:
                rec.state = "paid"
            elif rec.deu_date and rec.due_date < today:
                rec.state = "overdue"
            else:
                rec.state = "due"
