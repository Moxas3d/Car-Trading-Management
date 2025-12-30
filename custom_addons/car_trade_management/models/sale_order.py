from odoo import models, fields


class Sale(models.Model):
    _name = "car.trading.sale.order"
    _description = "Car Sale"

    name = fields.Char(default="New")
    customer_id = fields.Many2one("car.trading.partner")
    car_id = fields.Many2one("car.trading.car")

    sale_price = fields.Float()
    payment_type = fields.Selection(
        [
            ("cash", "Cash"),
            ("installment", "Installment"),
        ]
    )
    installment_strategy_id = fields.Many2one(
        "car.trading.installment.strategy", required=True
    )

    installment_ids = fields.One2many(
        "car.trading.installment", "sale_id", domain=[("installment_type", "=", "sale")]
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("delivered", "Delivered"),
        ],
        default="draft",
    )
