from odoo import models, fields


class Partner(models.Model):
    _name = "car.trading.partner"
    _description = "Vendor / Customer"

    name = fields.Char(required=True)
    partner_type = fields.Selection(
        [
            ("vendor", "Vendor"),
            ("customer", "Customer"),
        ],
        required=True,
    )

    phone = fields.Char()
    description = fields.Text()
