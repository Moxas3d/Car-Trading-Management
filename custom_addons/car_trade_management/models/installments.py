from odoo import models, fields


class CarTradingInstallment(models.Model):
    _name = "car.trading.installment"
    _description = "Car Trading Installment"
    _order = "due_date"

    partner_id = fields.Many2one("car.trading.partner", required=True, readonly=True)
    installment_type = fields.Selection(
        [
            ("purchase", "Purchase"),
            ("sale", "Sale"),
        ],
        required=True,
    )

    purchase_id = fields.Many2one(
        "car.trading.purchase.order", string="Purchase Order", ondelete="cascade"
    )

    sale_id = fields.Many2one(
        "car.trading.sale.order", string="Sale Order", ondelete="cascade"
    )

    amount = fields.Float(required=True)
    due_date = fields.Date(required=True)
    paid = fields.Boolean(default=False)

    state = fields.Selection(
        [("draft", "Draft"), ("due", "Due"), ("overdue", "Overdue"), ("paid", "Paid")]
    )
