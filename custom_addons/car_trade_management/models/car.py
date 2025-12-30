from odoo import models, fields


class Car(models.Model):
    _name = "car.trading.car"
    _description = "Car"

    name = fields.Char(required=True)
    vin = fields.Char(string="VIN", required=True, size=17)
    brand = fields.Char()
    model = fields.Char()
    year = fields.Integer()
    purchase_price = fields.Float()
    sale_price = fields.Float()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("purchased", "Purchased"),
            ("available", "Available for Sale"),
            ("sold", "Sold"),
        ],
        default="draft",
    )

    _sql_constraints = [
        (
            "unique_vin",
            "unique(vin)",
            "The Vehicle Identification Number (VIN) number must be unique!",
        )
    ]
