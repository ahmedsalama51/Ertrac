# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import io
import base64

class TaskErtracXlsxs(models.AbstractModel):
    _name = 'report.report_timesheet_ertrac.report_task2_ertrac'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, task_ids):
        report_name = "محضر حصر أعمال"
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
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:X', 15)
        bold = workbook.add_format({'bold': True})
        bold.set_font_size(13)
        bold_center = workbook.add_format({'bold': True, 'align': 'center'})
        bold_center.set_font_size(13)
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        bold_right.set_font_size(13)
        
        # Company Logo
        company_logo = self.env.user.company_id.logo
        imgdata = base64.b64decode(company_logo)
        image = io.BytesIO(imgdata)
        worksheet.insert_image('D1', 'myimage.png', {'image_data': image,'x_scale': 1, 'y_scale': 0.5})
        
        worksheet.merge_range(4, 1, 4, 4, "محضر حصر أعمال", bold_center)
        worksheet.merge_range(5, 1, 5, 6, "الأعمال التي قامت بتنفيذها الشركة المصرية لتجديد و صيانة خطوط السكك الحديدية", bold_center)
        worksheet.merge_range(6, 1, 6, 6, "أعمال الصيانة الميكانيكية ما بين        بالخط الطالع والنازل      التابع لإدارة هندسة    خلال شهر   ", bold_center)
        worksheet.merge_range(7, 1, 7, 2, "اليوم %s" % fields.Date.today(), bold)
        worksheet.merge_range(7, 5, 7, 6, "إجتمعنا نحن كلا من :")
        worksheet.write(8, 0, "-1")
        worksheet.merge_range(8, 1, 8, 2, "السيد المهندس/ ")
        worksheet.merge_range(8, 5, 8, 6, "رئيس قسم صيانة هندسة السكة")
        worksheet.write(9, 0, "-2")
        worksheet.merge_range(9, 1, 9, 2, "السيد المهندس/ ")
        worksheet.merge_range(9, 5, 9, 6, "هندسة منطقة")
        worksheet.write(10, 0, "-3")
        worksheet.merge_range(10, 1, 10, 2, " السيــد/")
        worksheet.merge_range(10, 5, 10, 6, "مندوب الشركة المصرية")
        worksheet.merge_range(11, 1, 11, 6, "وبالمرور والمعاينة على الطبيعة تبين ان الشركة قامت بأعمال الصيانة الميكانيكية ما بين    بالخطين الطالع والنازل ", bold_center)
        worksheet.merge_range(12, 1, 12, 6, "بقسم هندسة    التابع لإدارة هندسة   :")
        cell_format_header = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_format_total = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#FFC7CE'})
        cell_format_total2 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#C6EFCE'})
        cell_format_header.set_center_across()
        
        worksheet.merge_range(14, 0, 15, 0, '')
        worksheet.merge_range(14, 1, 15, 1, 'بيان الأعمال', cell_format_header)
        worksheet.merge_range(14, 2, 15, 2, 'من كم', cell_format_header)
        worksheet.merge_range(14, 3, 15, 3, 'إلى كم', cell_format_header)
        worksheet.merge_range(14, 4, 15, 4, 'بطول', cell_format_header)
        row = 15
        tasks_arranged_increase = []
        tasks_arranged_decrease = []
        tasks_arranged_odd = []

        for idx , task in enumerate(task_ids):
            for idxx , timesheet_ids in enumerate(task.timesheet_ids):
                    if timesheet_ids.line_type == 'increase_line' :
                          tasks_arranged_increase.append(timesheet_ids)
                        
        for idx , task in enumerate(task_ids):
            for idxx , timesheet_ids in enumerate(task.timesheet_ids):
                    if timesheet_ids.line_type == 'decrease_line' :
                          tasks_arranged_decrease.append(timesheet_ids)
                            
        for idx , task in enumerate(task_ids):
            for idxx , timesheet_ids in enumerate(task.timesheet_ids):
                    if timesheet_ids.line_type == 'odd_line' :
                          tasks_arranged_odd.append(timesheet_ids)
                                
        row_initial = row 
        # if Increased Line available
        if tasks_arranged_increase:
             for idxx, timesheet_ids in enumerate(tasks_arranged_increase):
                     row += 1
                     col = 0
                     worksheet.write(row, col, '')
                     col += 1
                     worksheet.write(row, col, 'الخط الطالع', cell_format_row)
                     col += 1
                     worksheet.write(row, col, timesheet_ids.from_km, cell_format_row)
                     col += 1
                     worksheet.write(row, col, timesheet_ids.to_km, cell_format_row)
                     col += 1
                     worksheet.write(row, col, timesheet_ids.total_km, cell_format_row)
             worksheet.merge_range(row_initial+1, 1, row , 1, 'الخط الطالع',cell_format_row)
             # Final Total
             row += 1
             col = 0
             worksheet.write(row, col, '')
             col += 1
             worksheet.write(row, col, 'إجمالي الخط الطالع', cell_format_total)
             col += 1
             worksheet.write(row, col, '' ,cell_format_total)
             col += 1
             worksheet.write(row, col, '' ,cell_format_total)
             col += 1
             worksheet.write(row, col, sum(c.total_km for c in tasks_arranged_increase), cell_format_total)
        row_initial2 = row 
        if tasks_arranged_decrease:
              for idxx, timesheet_ids in enumerate(tasks_arranged_decrease):
                      row += 1
                      col = 0
                      worksheet.write(row, col, '')
                      col += 1
                      worksheet.write(row, col, 'الخط النازل', cell_format_row)
                      col += 1
                      worksheet.write(row, col, timesheet_ids.from_km, cell_format_row)
                      col += 1
                      worksheet.write(row, col, timesheet_ids.to_km, cell_format_row)
                      col += 1
                      worksheet.write(row, col, timesheet_ids.total_km, cell_format_row)
              worksheet.merge_range(row_initial2+1, 1, row , 1, 'الخط النازل',cell_format_row)
              # Final Total
              row += 1
              col = 0
              worksheet.write(row, col, '')
              col += 1
              worksheet.write(row, col, ' إجمالي الخط النازل', cell_format_total)
              col += 1
              worksheet.write(row, col, '' ,cell_format_total)
              col += 1
              worksheet.write(row, col, '' ,cell_format_total)
              col += 1
              worksheet.write(row, col, sum(c.total_km for c in tasks_arranged_decrease), cell_format_total)
        row_initial = row
        if tasks_arranged_odd:
              for idxx, timesheet_ids in enumerate(tasks_arranged_odd):
                      row += 1
                      col = 0
                      worksheet.write(row, col, '')
                      col += 1
                      worksheet.write(row, col, 'الخط المفرد', cell_format_row)
                      col += 1
                      worksheet.write(row, col, timesheet_ids.from_km, cell_format_row)
                      col += 1
                      worksheet.write(row, col, timesheet_ids.to_km, cell_format_row)
                      col += 1
                      worksheet.write(row, col, timesheet_ids.total_km, cell_format_row)
              worksheet.merge_range(row_initial+1, 1, row , 1, 'الخط المفرد',cell_format_row)
              # Final Total
              row += 1
              col = 0
              worksheet.write(row, col, '')
              col += 1
              worksheet.write(row, col, 'إجمالي الخط المفرد', cell_format_total)
              col += 1
              worksheet.write(row, col, '' ,cell_format_total)
              col += 1
              worksheet.write(row, col, '' ,cell_format_total)
              col += 1
              worksheet.write(row, col, sum(c.total_km for c in tasks_arranged_odd), cell_format_total)
        tasks_total = tasks_arranged_decrease + tasks_arranged_increase + tasks_arranged_odd
        # Final Total
        row += 1
        col = 0
        worksheet.write(row, col, '')
        col += 1
        worksheet.write(row, col, 'الإجمالي', cell_format_total2)
        col += 1
        worksheet.write(row, col, '' ,cell_format_total2)
        col += 1
        worksheet.write(row, col, '' ,cell_format_total2)
        col += 1
        worksheet.write(row, col, math.floor(sum(c.total_km for c in tasks_total)), cell_format_total2)
        #line total
        row += 1
        worksheet.merge_range(row, 1, row , 5, "بإجمالي مسافة طالع , نازل = %s  كم" % sum(c.total_km for c in tasks_total) , bold_center)
        # Lines user will write in
        row += 6
        # Footer
        row += 2
        worksheet.merge_range(row, 0, row, 5, "جميع الأعمال تمت طبقا للأصول الفنية للهيئة وبحالة جيدة", bold_center)
        row += 1
        worksheet.merge_range(row, 1, row, 5, "وتحرر هذا المحضر منا بذلك", bold_center)
        row += 1
        worksheet.write(row, 1, "مندوب الشركه", bold_center)
        row += 1
        worksheet.merge_range(row-1, 4, row-1, 5, "مندوب الهيئه", bold_center)

        row += 4
        worksheet.merge_range(row, 1, row, 6, "يعتمد / ", bold_center)
        row += 1
        worksheet.merge_range(row, 1, row, 6,"رئيس مجلس الاداره والعضو المنتدب ", bold_center)
        row += 1
        worksheet.merge_range(row, 1, row, 6,"مهندس / مصطفى عبداللطيف أبوالمكارم ", bold_center)
