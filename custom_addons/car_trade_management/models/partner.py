from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    partner_type = fields.Selection(
        [
            ("vendor", "Vendor"),
            ("customer", "Customer"),
        ],
        required=True,
    )
