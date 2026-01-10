from odoo import http, models
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval
from odoo.exceptions import ValidationError
from datetime import date


def format_string(value: str) -> str:
    return " ".join(word.capitalize() for word in value.split("_"))


def get_model_name(model_name):
    if model_name in ("car.trading.bank"):
        return {
            "model_name": model_name,
            "fields": ("name", "interest_rate", "max_installment_months", "notes"),
        }
    else:
        raise ValidationError("Not allowed for this model")


class XlsxReport(http.Controller):
    @http.route(
        "/excel/report/<string:model_name>/<string:model_ids>",
        type="http",
        methods=["GET"],
        auth="user",
    )
    def download_model_excel_report(self, model_name, model_ids):
        model = get_model_name(model_name)
        model_ids = request.env[model["model_name"]].browse(literal_eval(model_ids))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet(f"Records for {model['model_name']}")

        header_format = workbook.add_format(
            {"bold": True, "bg_color": "#D3D3D3", "border": 1, "align": "center"}
        )
        string_format = workbook.add_format(
            {
                "border": 1,
                "align": "center",
                "bg_color": "#D3D3D3",
            }
        )
        field_names = model["fields"]

        for col_num, header in enumerate(field_names):
            worksheet.write(0, col_num, format_string(header), header_format)

        row_num = 1
        for rec in model_ids:
            for col_num, field_name in enumerate(field_names):
                value = rec[field_name]
                # Handle different data types if necessary
                if isinstance(value, models.BaseModel):
                    value = value.display_name
                worksheet.write(row_num, col_num, value if value else "", string_format)
            row_num += 1

        workbook.close()
        output.seek(0)
        file_name = f"{model['model_name']} Report - {date.today()}.xlsx"
        return request.make_response(
            output.getvalue(),
            headers=[
                (
                    "Content-Type",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
                ("Content-Disposition", f"attachment; filename={file_name}"),
            ],
        )
