from odoo import models, fields


class Purchase(models.Model):
    _name = "purchase"
    _description = "Car Purchase"

    name = fields.Char(default="New")
    vendor_id = fields.Many2one("partner")
    car_ids = fields.One2many("car")

    total_amount = fields.Float()
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
            ("done", "Done"),
        ],
        default="draft",
    )
