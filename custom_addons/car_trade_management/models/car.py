from odoo import models, fields


class Car(models.Model):
    _name = "car"
    _description = "Car"

    name = fields.Char(required=True)
    vin = fields.Char(string="VIN", required=True, size=17)
    brand = fields.Char()
    model = fields.Char()
    year = fields.Integer()
    cost_price = fields.Float()
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


# Draft The record is just created; it’s a "work in progress" and hasn't been confirmed yet.
# Purchased The item has been bought from a supplier and is likely on its way or being processed.
# Available for SaleThe item is now in stock and ready for a customer to buy.
#
#
# 1. VIN vs. Model
# If you have ten "2023 Toyota Camrys" on your lot:
# The brand will be "Toyota" for all ten.
# The model will be "Camry" for all ten.
# The year will be "2023" for all ten.
# The vin will be different for every single one of those ten cars.
