from odoo import models, fields


class Purchase(models.Model):
    _name = "car.trading.purchase.order"
    _description = "Car Purchase"

    name = fields.Char(default="New")
    vendor_id = fields.Many2one("car.trading.partner")
    number_of_cars = fields.Integer()
    car_ids = fields.One2many("car.trading.car")
    total_purchase_price = fields.Float()
    cost_per_car = fields.Float()

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
