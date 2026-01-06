from odoo import models, fields, api


class Purchase(models.Model):
    _name = "car.trading.purchase.order"
    _description = "Car Purchase"

    name = fields.Char(default="New")
    vendor_id = fields.Many2one("res.partner", domain=[("partner_type", "=", "vendor")])
    car_ids = fields.One2many("car.trading.car", "purchase_order_id", string="Cars")

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
    )

    number_of_cars = fields.Integer(
        compute="_compute_purchase_totals",
        store=True,
    )

    total_purchase_price = fields.Float(
        compute="_compute_purchase_totals",
        store=True,
    )

    @api.depends("car_ids.purchase_price")
    def _compute_purchase_totals(self):
        for rec in self:
            cars = rec.car_ids
            rec.number_of_cars = len(cars)
            rec.total_purchase_price = sum(cars.mapped("purchase_price"))
