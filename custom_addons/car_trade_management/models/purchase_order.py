from odoo import models, fields


class Purchase(models.Model):
    _name = "car.trading.purchase.order"
    _description = "Car Purchase"

    name = fields.Char(default="New")
    vendor_id = fields.Many2one("car.trading.partner")
    car_ids = fields.One2many("car.trading.car")

    total_amount = fields.Float()

    paid_amount = fields.Float()  # computed
    remaining_amount = fields.Float()  # computed

    installment_ids = fields.One2many(
        "car.trading.installment",
        "purchase_id",
        domain=[("installment_type", "=", "purchase")],
    )

    payment_type = fields.Selection(
        [
            ("cash", "Cash"),
            ("installment", "Installment"),
        ]
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("in_payment", "In Installments"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
    )


# down_payment = fields.Float()
