from odoo import api, fields, models


class PurchaseXlsx(models.AbstractModel):
    _name = 'report.purchase_request.report_purchase_request_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, purchase):
        format_1 = workbook.add_format({'bold': True, 'align': 'center'})

        row = 0
        col = 0

        print('saaaaaaaaaaaaaaa', self)
        print('saaaaaaaaaaaaaaa', workbook)
        print('saaaaaaaaaaaaaaa', purchase)

        for obj in purchase:
            date_default_col1_style = workbook.add_format(
                {'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2,
                 'num_format': 'yyyy-mm-dd'})
            report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet(report_name[:31])
            sheet.set_column('A:A', 12)
            sheet.set_column('B:B', 14)
            sheet.set_column('C:C', 14)
            sheet.set_column('D:D', 12)
            sheet.set_column('E:E', 12)
            sheet.set_column('F:F', 12)
            sheet.set_column('G:G', 12)
            bold = workbook.add_format({'bold': True})

            sheet.write(row, col, 'Name', bold)
            sheet.write(row + 1, col, obj.name)

            col += 1
            sheet.write(row, col, 'Start Date', bold)
            sheet.write_datetime(row + 1, col, obj.date_start, date_default_col1_style)

            col += 1
            sheet.write(row, col, 'End Date', bold)
            # sheet.write(row + 1, col, obj.date_end)
            sheet.write_datetime(row + 1, col, obj.date_end, date_default_col1_style)

            for line in obj.order_line_ids:
                col += 1
                sheet.write(row, col, 'Product Name', bold)
                sheet.write(row + 1, col, line.description)

                col += 1
                sheet.write(row, col, 'Quantity', bold)
                sheet.write(row + 1, col, line.quantity)

                col += 1
                sheet.write(row, col, 'Cost Price', bold)
                sheet.write(row + 1, col, line.cost_price)

                col += 1
                sheet.write(row, col, 'Total Cost', bold)
                sheet.write(row + 1, col, line.total)




