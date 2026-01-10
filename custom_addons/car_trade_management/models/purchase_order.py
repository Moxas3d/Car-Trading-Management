from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Purchase(models.Model):
    _name = "car.trading.purchase.order"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Car Purchase"

    name = fields.Char(default="New", readonly=True)
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
        tracking=True,
    )

    number_of_cars = fields.Integer(
        compute="_compute_purchase_totals",
        store=True,
    )

    total_purchase_price = fields.Float(
        compute="_compute_purchase_totals",
        store=True,
    )

    vendor_count = fields.Integer(compute="_compute_vendor_count")

    def _compute_vendor_count(self):
        for record in self:
            record.vendor_count = 1 if record.vendor_id else 0

    def action_open_vendor(self):
        return {
            "name": "Vendor",
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "view_mode": "form",
            "res_id": self.vendor_id.id,
            "target": "current",
        }

    def action_open_cars(self):
        return {
            "name": "Cars",
            "type": "ir.actions.act_window",
            "res_model": "car.trading.car",
            "view_mode": "list,form",
            "domain": [("id", "in", self.car_ids.ids)],
            "target": "current",
        }

    @api.depends("car_ids.purchase_price")
    def _compute_purchase_totals(self):
        for rec in self:
            cars = rec.car_ids
            rec.number_of_cars = len(cars)
            rec.total_purchase_price = sum(cars.mapped("purchase_price"))

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = (
                self.env["ir.sequence"].next_by_code("car.trading.purchase.order")
                or "New"
            )
        return super().create(vals)

    def _check_before_confirm(self):
        for rec in self:
            if not rec.car_ids:
                raise ValidationError("You must add at least one car.")

            vins = rec.car_ids.mapped("vin")
            if any(not vin for vin in vins):
                raise ValidationError("All cars must have a VIN.")

            if len(vins) != len(set(vins)):
                raise ValidationError("Duplicate VINs are not allowed.")

    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                continue

            rec._check_before_confirm()

            rec.state = "confirmed"

            rec.car_ids.write(
                {
                    "state": "purchased",
                }
            )

    def action_done(self):
        for rec in self:
            if rec.state != "confirmed":
                continue

            rec.state = "done"

            rec.car_ids.write(
                {
                    "state": "available",
                }
            )

    def action_cancel(self):
        for rec in self:
            if rec.state == "done":
                raise ValidationError(
                    "You cannot cancel a purchase order with sold cars."
                )

            rec.state = "cancel"
            rec.car_ids.write({"state": "draft"})
