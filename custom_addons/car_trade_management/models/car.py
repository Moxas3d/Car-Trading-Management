from odoo import models, fields, api


class Car(models.Model):
    _name = "car.trading.car"
    _description = "Car"

    name = fields.Char(default="New", readonly=True)

    vin = fields.Char(string="VIN", required=True, size=17)
    brand = fields.Char()
    model = fields.Char()
    year = fields.Integer()

    purchase_order_id = fields.Many2one("car.trading.purchase.order")
    sale_order_id = fields.Many2one("car.trading.sale.order")

    purchase_price = fields.Float(required=True)
    sale_price = fields.Float(related="sale_order_id.sale_price", store=True)

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

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = (
                self.env["ir.sequence"].next_by_code("car.trading.car") or "New"
            )
        return super().create(vals)
