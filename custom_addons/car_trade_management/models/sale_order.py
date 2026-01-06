from odoo import models, fields, api


class SaleOrder(models.Model):
    _name = "car.trading.sale.order"
    _description = "Car Sale"

    name = fields.Char(default="New")
    customer_id = fields.Many2one(
        "res.partner", domain=[("partner_type", "=", "customer")]
    )
    car_id = fields.Many2one("car.trading.car")

    sale_price = fields.Float()
    payment_type = fields.Selection(
        [
            ("cash", "Cash"),
            ("installment", "Installment"),
        ]
    )
    installment_strategy_id = fields.Many2one(
        "car.trading.installment.strategy", required=False
    )

    installment_ids = fields.One2many("car.trading.installment", "sale_id")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("delivered", "Delivered"),
            ("done", "Done"),
        ],
        default="draft",
    )

    bank_id = fields.Many2one(
        related="installment_strategy_id.bank_id",
        store=True,
        readonly=True,
    )

    installment_months = fields.Integer(
        related="installment_strategy_id.months",
        store=True,
        readonly=True,
    )

    down_payment_percent = fields.Float(
        related="installment_strategy_id.down_payment_percent",
        store=True,
        readonly=True,
    )

    bank_interest_amount = fields.Float(
        related="installment_strategy_id.bank_interest_amount",
        store=True,
        readonly=True,
    )

    company_funding_amount = fields.Float(
        related="installment_strategy_id.company_funding_amount",
        store=True,
        readonly=True,
    )

    is_funded = fields.Boolean(
        related="installment_strategy_id.is_funded",
        store=True,
        readonly=True,
    )

    remaining_amount = fields.Float(
        string="Remaining Amount",
        compute="_compute_remaining_amount",
        store=True,
    )

    @api.depends(
        "payment_type",
        "installment_ids.amount",
        "installment_ids.paid",
    )
    def _compute_remaining_amount(self):
        for rec in self:
            # Cash payment → no remaining amount
            if rec.payment_type != "installment":
                rec.remaining_amount = 0.0
                continue

            unpaid_installments = rec.installment_ids.filtered(lambda i: not i.paid)

            rec.remaining_amount = sum(unpaid_installments.mapped("amount"))
