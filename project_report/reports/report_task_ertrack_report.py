# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning
import io
import base64


# Ahmed Salama Code Start ---->


class TaskErtrackXlsx(models.AbstractModel):
    _name = 'report.egymentors_ertrack_report.report_task_ertrack'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, parent_tasks):
        report_name = "محضر الحصر"
        # One sheet by partner
        worksheet = workbook.add_worksheet(report_name[:31])
        format_left_to_right = workbook.add_format()
        format_left_to_right.set_reading_order(1)

        format_right_to_left = workbook.add_format()
        format_right_to_left.set_reading_order(2)
        cell_format_right = workbook.add_format()
        cell_format_right.set_align('right')

        worksheet.right_to_left()
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 50)
        worksheet.set_column('C:X', 5)
        bold = workbook.add_format({'bold': True})
        bold_center = workbook.add_format({'bold': True, 'align': 'center'})
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        
        # Company Logo
        company_logo = self.env.user.company_id.logo
        imgdata = base64.b64decode(company_logo)
        image = io.BytesIO(imgdata)
        worksheet.insert_image('M1', 'myimage.png', {'image_data': image,'x_scale': 1, 'y_scale': 0.5})
        
        invoice = []
        for idx , task in enumerate(parent_tasks):
            invoice = self.env['account.move'].search([('invoice_origin','=',task.sale_line_id.order_id.name)],limit = 1)
            if invoice:
                break
                
        
        worksheet.merge_range(3, 3, 3, 7,'محضر حصر أعمال جاري (%s)'% invoice.current ,bold_center)
        worksheet.merge_range(4, 2, 4, 13, 'الأعمال التي قامت بتنفيذها الشركة المصرية لتجديد وصيانة خطوط السكك الحديدية',bold_center)
        worksheet.merge_range(5, 2, 5, 14, 'أعمال لتعديلات حوش محطة     بخط       قسم      التابع لإدارة هندسة السكك    شهر    2020',bold_center)
#         worksheet.merge_range(6, 1, 6, 3, "%s محضر الحصر بتاريخ" % fields.Date.today(), bold)
        cell_format_header = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_header_wrap = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_header_wrap.set_text_wrap()
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_format_row_wrap = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_format_row_wrap.set_text_wrap()
        
        cell_format_header.set_center_across()
        cell_format_header.set_font_size(7)
        cell_format_row.set_font_size(7)
        
        cell_format_header_wrap.set_center_across()
        cell_format_header_wrap.set_font_size(7)
        cell_format_row_wrap.set_font_size(7)
        row = 6

        for idx, task in enumerate(parent_tasks):
            col = 0
            worksheet.merge_range(row, col, row + 1, col, 'م', cell_format_header)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'بيان الأعمال', cell_format_header)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'الوحده', cell_format_header)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'الكميه', cell_format_header)
            col += 1
            if task.task_header_id:
                percentages = task.task_header_id.line_ids.mapped('percent')
                last_col = col + len(percentages)
                last_col = 15
                # Total Col
                worksheet.merge_range(row, last_col, row + 1, last_col, ' النسب  السابقة المنصرفة',
                                      cell_format_header_wrap)
                worksheet.merge_range(row, last_col+1, row + 1, last_col+1, 'النسب المستجدة',
                                      cell_format_header_wrap)
                worksheet.merge_range(row, last_col+2, row + 1, last_col+2, 'إجمالى النسبة المستحقة الصرف',
                                      cell_format_header_wrap)
                # Headers Part
                worksheet.merge_range(row, col, row, last_col - 1,
                                      ' النسب المئويه لبنود الأعمال طبقا" للعقد رقم 1 لسنة 2018/2017 %s' % (task.report_description)
                                      , cell_format_header)
                row += 1
#                 for y, line in enumerate(task.task_header_id.line_ids):
#                     worksheet.write(row, col+y, "%s %s%s" % (line.name, line.percent, "%")
#                                     , cell_format_header)
                
                if len(percentages) == 11:
                    for y, line in enumerate(task.task_header_id.line_ids):
                          worksheet.write(row, col+y, "%s %s%s" % (line.name, line.percent, "%")
                                          , cell_format_header_wrap)
                elif len(percentages) == 10:
                    for y, line in enumerate(task.task_header_id.line_ids):
                        if y == 9:
#                             worksheet.merge_range(1,y+col,1,y+col+1,'y= %s  col = %s   line = %s' % (y,col,line.name))
                            worksheet.merge_range(row, col+y, row, col+y+1, "%s %s%s" % (line.name, line.percent, "%")
                                          , cell_format_header_wrap)
                            break
                        else:
#                             worksheet.write(0,0,'y= %s  col = %s   line = %s' % (y,col,line.name))
                            worksheet.write(row, col+y, "%s %s%s" % (line.name, line.percent, "%")
                                          , cell_format_header_wrap)
                elif len(percentages) == 8:
                    wrap = 0
                    for y, line in enumerate(task.task_header_id.line_ids): 
                        if y == 5 or y == 6 or y == 7:
                            worksheet.merge_range(row, col+y+wrap, row, col+y+wrap+1, "%s %s%s" % (line.name, line.percent, "%")
                                          , cell_format_header_wrap)
                            wrap += 1
                            
                        else:
#                             worksheet.write(0,0,'y= %s  col = %s   line = %s' % (y,col,line.name))
                            worksheet.write(row, col+y, "%s %s%s" % (line.name, line.percent, "%")
                                          , cell_format_header_wrap)
                elif len(percentages) == 6:
                    wrap = 0
                    for y, line in enumerate(task.task_header_id.line_ids): 
                        if y != 5 :
                            worksheet.merge_range(row, col+y+wrap, row, col+y+wrap+1, "%s %s%s" % (line.name, line.percent, "%")
                                          , cell_format_header_wrap)
                            wrap += 1
                            
                        else:
#                             worksheet.write(0,0,'y= %s  col = %s   line = %s' % (y,col,line.name))
                            worksheet.write(row, col+y+5, "%s %s%s" % (line.name, line.percent, "%")
                                          , cell_format_header_wrap)
                elif len(percentages) == 4:
                    wrap = 0
                    for y, line in enumerate(task.task_header_id.line_ids):
                        if y !=3 :
                             worksheet.merge_range(row, col+y+wrap, row, col+y+wrap+2, "%s %s%s" % (line.name, line.percent, "%")
                                               , cell_format_header_wrap)
                             wrap += 2
                        else:
                            worksheet.merge_range(row, col+y+wrap, row, col+y+wrap+1, "%s %s%s" % (line.name, line.percent, "%")
                                               , cell_format_header_wrap)
                            wrap += 1
                            
                            
                row += 1
#                 elif len(percentages) == 8:
#                     for y, line in enumerate(task.task_header_id.line_ids):
#                         if y == 1 or y==2 or y==3 :
#                             worksheet.merge_range(row, col+y, row, col+1+y, "%s %s%s" % (line.name, line.percent, "%")
#                                           , cell_format_header)
                            
#                         worksheet.write(row, col+1+y, "%s %s%s" % (line.name, line.percent, "%")
#                                           , cell_format_header)
                # Main Task Name Line
#                 worksheet.write(row, 0, idx+1, cell_format_header)
                worksheet.write(row, 1, task.name, cell_format_header)
                worksheet.merge_range(row, 2, row, last_col + 2,
                                      ' ', cell_format_header)
                
                invoice_per_task = self.env['account.move'].search([('invoice_origin','=',task.sale_line_id.order_id.name)],limit = 1)
                row_task = row

                # Sub Tasks Lines
                for idxx, child_task in enumerate(task.child_ids):
                    row += 1
                    col = 0
#                     worksheet.write(row, col, invoice.current, cell_format_row)
                    col += 1
                    worksheet.write(row, col, child_task.name, cell_format_row)
                    col += 1
                    worksheet.write(row, col,child_task.sale_line_id.product_uom.name, cell_format_row)
                    col += 1
                    worksheet.write(row, col, child_task.effective_hours, cell_format_row)
                    col += 1
                    if len(percentages) == 11: 
                        for p, percent in enumerate(percentages):
                            worksheet.write(row, col, percent, cell_format_row)
                            col += 1
                        
                    elif len(percentages) == 10:
                        for p, percent in enumerate(percentages):
                            if p == 9:
                                worksheet.merge_range(row, col, row, col+1, percent, cell_format_row)
                                col += 1
                                break
                            else:
                              worksheet.write(row, col, percent, cell_format_row)
                              col += 1
                    elif len(percentages) == 8:
                        wrap = 0
                        for p, percent in enumerate(percentages):
                            if p == 5 or p == 6 or p == 7 :
                                worksheet.merge_range(row, col+wrap, row, col+wrap+1, percent, cell_format_row)
                                col += 1
                                wrap += 1
                            else:
                              worksheet.write(row, col, percent, cell_format_row)
                              col += 1
                    elif len(percentages) == 6:
                        wrap = 0
                        for p, percent in enumerate(percentages):
                            if p != 5 :
                                worksheet.merge_range(row, col+wrap, row, col+wrap+1, percent, cell_format_row)
                                col += 1
                                wrap += 1
                            else:
                              worksheet.write(row, col+5, percent, cell_format_row)
                              col += 1
                    elif len(percentages) == 4:
                        wrap = 0
                        for p, percent in enumerate(percentages):
                            if p != 3:
                                worksheet.merge_range(row, col+wrap, row, col+wrap+2, percent, cell_format_row)
                                col += 1
                                wrap += 2
                            else:
                                worksheet.merge_range(row, col+wrap, row, col+wrap+1, percent, cell_format_row)
                                col += 1
                                wrap += 2
                                
                        # Total Col

                    worksheet.write(row, last_col, "%s%s" % (task.task_header_id.previous, "%"),
                                    cell_format_row)
                    col += 1
                    worksheet.write(row, last_col+1, "%s%s" % (task.task_header_id.new, "%"),
                                    cell_format_row)
                    col += 1
                    worksheet.write(row, last_col+2, "%s%s" % (task.task_header_id.total, "%"),
                                    cell_format_row)
            else:
                raise Warning(_("Task Header Is missing"))
            # Final Total
            row += 1
            col = 0
#             worksheet.write(row, col, invoice.current, cell_format_header_wrap)
            col += 1
            worksheet.write(row, col, 'الإجمالي', cell_format_row)
            col += 1
            worksheet.write(row, col, task.sale_line_id.product_uom.name , cell_format_row)
            col += 1
            worksheet.write(row, col, sum(c.effective_hours for c in task.child_ids), cell_format_row)
            row += 1
#         worksheet.merge_range(row, 0, row, 2, " = أعمال شحن ناتج الفج للسكك والمفاتيح بعربات برية ونقلها للمقالب العمومية ", bold_right)
        worksheet.merge_range(8, 0, row-1, 0, invoice.current, cell_format_header_wrap)
        worksheet.merge_range(row, 10, row, 17, "طبقا لمحضر حصر الأعمال بالموقع والمرفق صورته", bold_right)
        # Footer
        row += 2
        worksheet.write(row, 1, "مندوب الشركه المنفذ", bold_center)
        worksheet.merge_range(row+1, 0, row+1, 1, "السيد/ ناصر بشاي عبدالشهيد", bold_center)

        worksheet.merge_range(row, 3, row, 7, "مهندس منطقه سوهاج", bold_center)
        worksheet.merge_range(row+1, 3, row+1, 7, "م/ رحاب عبدالعال عبدالعزيز", bold_center)

        worksheet.merge_range(row-1, 9, row-1, 14, "مندوب الهيئه", bold_center)
        worksheet.merge_range(row, 9, row, 14, "رئيس قسم صيانه السكه سوهاج", bold_center)
        worksheet.merge_range(row+1, 9, row+1, 14, "م/ مدحت عيد صديق", bold_center)

        row += 4
        worksheet.merge_range(row, 3,row, 8, "يعتمد / ", bold_right)
        row += 1
        worksheet.merge_range(row, 3,row, 8, "رئيس مجلس الاداره والعضو المنتدب ", bold_right)
        row += 1
        worksheet.merge_range(row, 3,row, 8, "مهندس / مصطفى عبداللطيف أبوالمكارم ", bold_right)
        # Ahmed Salama Code End.
