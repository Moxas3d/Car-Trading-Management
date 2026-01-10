from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _name = "car.trading.sale.order"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Car Sale"

    name = fields.Char(default="New", readonly=True)

    customer_id = fields.Many2one(
        "res.partner",
        domain=[("partner_type", "=", "customer")],
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
            ("cancel", "Cancelled"),
        ],
        default="draft",
        tracking=True,
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

    bank_interest_rate = fields.Float(
        related="installment_strategy_id.bank_interest_rate",
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

    all_money_paid = fields.Boolean(
        compute="_compute_all_money_paid",
        store=True,
    )

    @api.depends(
        "payment_type",
        "installment_ids.amount",
        "installment_ids.paid",
    )
    def _compute_remaining_amount(self):
        for rec in self:
            if rec.payment_type != "installment":
                rec.remaining_amount = 0.0
                continue

            unpaid_installments = rec.installment_ids.filtered(lambda i: not i.paid)

            rec.remaining_amount = sum(unpaid_installments.mapped("amount"))

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = (
                self.env["ir.sequence"].next_by_code("car.trading.sale.order") or "New"
            )
        return super().create(vals)

    def _check_before_confirm(self):
        for rec in self:
            if not rec.car_id:
                raise ValidationError("You must select a car.")

            if rec.car_id.state != "available":
                raise ValidationError("The selected car is not available for sale.")

            if rec.sale_price <= 0:
                raise ValidationError("Sale price must be greater than zero.")

            if rec.payment_type == "installment":
                if not rec.installment_strategy_id:
                    raise ValidationError(
                        "Installment strategy is required for installment payments."
                    )

                bank = rec.installment_strategy_id.bank_id
                if (
                    bank
                    and rec.installment_strategy_id.months > bank.max_installment_months
                ):
                    raise ValidationError(
                        "Installment months exceed the bank's maximum allowed months."
                    )

    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                continue

            rec._check_before_confirm()

            rec.car_id.write(
                {
                    "state": "sold",
                    "sale_order_id": rec.id,
                }
            )

            rec.state = "confirmed"

            if rec.payment_type == "installment":
                rec._generate_installments()

    # def _generate_installments(self):
    #     for rec in self:
    #         rec.installment_ids.unlink()
    #
    #         months = rec.installment_strategy_id.months
    #         amount_per_installment = rec.sale_price / months
    #         start_date = fields.Date.today()
    #
    #         installments = []
    #         for i in range(1, months + 1):
    #             installments.append(
    #                 {
    #                     "sale_id": rec.id,
    #                     "sequence": i,
    #                     "amount": amount_per_installment,
    #                     "due_date": start_date + relativedelta(months=i),
    #                 }
    #             )
    #
    #         self.env["car.trading.installment"].create(installments)

    def _generate_installments(self):
        for rec in self:
            if rec.payment_type != "installment":
                continue

            strategy = rec.installment_strategy_id
            if not strategy or strategy.months <= 0:
                continue

            if not rec.sale_price or rec.sale_price <= 0:
                continue

            # # 1️⃣ Down payment
            # down_payment_percent = rec.down_payment_percent or 0.0
            # down_payment_amount = rec.sale_price * (down_payment_percent / 100.0)
            #
            # # 2️⃣ Interest calculation
            # bank_interest = (rec.sale_price - down_payment_amount) * (
            #     rec.bank_interest_rate / 100
            # ) or 0.0
            #
            # company_funding = rec.company_funding_amount or 0.0
            #
            # customer_interest = max(bank_interest - company_funding, 0.0)
            #
            # # 3️⃣ Final financed amount (customer debt)
            # financed_amount = rec.sale_price - down_payment_amount + customer_interest
            #

            # 1️⃣ Down payment
            down_payment_percent = rec.down_payment_percent or 0.0
            down_payment_amount = rec.sale_price * (down_payment_percent / 100.0)

            # 2️⃣ Interest calculation
            financed_base = rec.sale_price - down_payment_amount

            bank_interest = financed_base * (rec.bank_interest_rate / 100.0)
            company_funding = rec.company_funding_amount or 0.0

            customer_interest = max(bank_interest - company_funding, 0.0)

            # 3️⃣ Final financed amount
            financed_amount = financed_base + customer_interest

            if financed_amount <= 0:
                continue

            rec.installment_ids.unlink()

            # 4️⃣ Create installments
            amount_per_installment = financed_amount / strategy.months
            start_date = fields.Date.today()

            installments = []
            for i in range(1, strategy.months + 1):
                installments.append(
                    {
                        "sale_id": rec.id,
                        "sequence": i,
                        "amount": amount_per_installment,
                        "due_date": start_date + relativedelta(months=i),
                    }
                )

            self.env["car.trading.installment"].create(installments)

    def action_deliver(self):
        for rec in self:
            if rec.state != "confirmed":
                continue

            rec.state = "delivered"

            if rec.payment_type == "cash":
                rec.state = "done"

    @api.depends("installment_ids.paid")
    def _compute_all_money_paid(self):
        for rec in self:
            if rec.payment_type != "installment":
                rec.all_money_paid = True
            else:
                rec.all_money_paid = (
                    all(rec.installment_ids.mapped("paid"))
                    if rec.installment_ids
                    else False
                )

    def action_done(self):
        for rec in self:
            if rec.state != "delivered":
                raise ValidationError(
                    "Sale order must be delivered before it can be marked as done."
                )

            if rec.payment_type == "installment" and not rec.all_money_paid:
                raise ValidationError(
                    "All installments must be paid before closing the sale order."
                )

            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            paid_installments = rec.installment_ids.filtered(lambda i: i.paid)
            if paid_installments:
                raise ValidationError(
                    "You cannot cancel a sale order with paid installments."
                )

            rec.installment_ids.unlink()

            if rec.car_id:
                rec.car_id.write(
                    {
                        "state": "available",
                        "sale_order_id": False,
                    }
                )

            rec.state = "draft"
