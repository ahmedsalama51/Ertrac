# -*- coding: utf-8 -*-
import base64
import io
import calendar
from odoo import models, fields, _
from odoo.addons.project_report.wizard.work_progress_report import MONTHS
ORDER_LIST = ['أولا:', 'ثانياً:', 'ثالثا:', 'رابعا:ً', 'خامسا:ً', 'سادسا:ً', 'سابعاً:', 'ثامناً:']

# Ahmed Salama Code Start ---->


class ReportTimesheetWorkProgressXlsx(models.AbstractModel):
    _name = 'report.egymentors_ertrack_report.report_timesheet_work_progress'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, timesheets_ids):
        report_type = data.get('report_type')
        report_name = data.get('report_type_str')
        if report_type == 'report_1' and data.get('month'):
            report_name += " التى قامت بها الشركه المصريه من تجديد السكه عن شهر %s %s " \
                           % (data.get('month'), data.get('year'))
        if report_type == 'report_2' and data.get('month'):
            report_name += " خلال شهر %s %s طبقاً لخطه الهيئه " % (data.get('month'), data.get('year'))
        elif report_type == 'report_3' and data.get('year'):
            report_name += " لعام %s" % data.get('year')
            report_name += " طبقاً للبرنامج المعتمد من إستشارى الهيئه حتى %s" % data.get('to_date')
        elif report_type == 'report_4' and data.get('to_date'):
            report_name += " حتى %s" % data.get('to_date')
        elif report_type == 'report_5' and data.get('to_date'):
            report_name += " من %s إلى %s" % (data.get('date_from'), data.get('to_date'))
        elif report_type == 'report_6' and data.get('to_date'):
            report_name += " لعام %s" % data.get('year')
        elif report_type == 'report_7' and data.get('to_date'):
            report_name += " لصاينه وتجديد خطوط السكك الحديديه عامى %s/%s" % (data.get('year'), data.get('year2'))
        # One sheet by partner
        workbook.set_properties({
            'title': report_name,
            'subject': report_name,
            'author': 'Ahmed Salama',
            'company': 'of Wolves',
            'keywords': 'Timesheet, Sales, Project',
            'comments': 'Created with Python and XlsxWriter'})
        worksheet = workbook.add_worksheet(report_name[:31])
        format_left_to_right = workbook.add_format()
        format_left_to_right.set_reading_order(1)
        
        format_right_to_left = workbook.add_format()
        format_right_to_left.set_reading_order(2)
        cell_format_right = workbook.add_format()
        cell_format_right.set_align('right')
        
        worksheet.right_to_left()
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 30)
        last_detail_column = [4, "E"]
        comments_column = [5, "F"]
        if report_type in ['report_1', 'report_2']:
            last_detail_column = [4, "E"]
            comments_column = [5, "F"]
        if report_type in ['report_3', 'report_4']:
            last_detail_column = [7, "H"]
            comments_column = [8, "I"]
        if report_type in ['report_6', 'report_7']:
            last_detail_column = [14, "O"]
            comments_column = [15, "P"]
        
        worksheet.set_column('C:%s' % last_detail_column[1], 10)
        worksheet.set_column('%s:%s' % (comments_column[1], comments_column[1]), 40)
        bold = workbook.add_format({'bold': True})
        bold_center = workbook.add_format({'bold': True, 'align': 'center'})
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        
        # Company Logo
        company_logo = self.env.user.company_id.logo
        imgdata = base64.b64decode(company_logo)
        image = io.BytesIO(imgdata)
        worksheet.insert_image('F1', 'myimage.png', {'image_data': image, 'x_scale': 1, 'y_scale': 0.5})
        worksheet.merge_range(2, 0, 2, 4, report_name, bold_center)
        worksheet.merge_range(3, 0, 3, 1, "%s بتاريخ" % fields.Date.today(), bold)
        cell_format_header_parent = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                         'border': 1, 'fg_color': '#898a8c'})
        rotate_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                         'border': 1, 'fg_color': '#898a8c'})
        cell_format_header_yellow = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                         'border': 1, 'fg_color': 'yellow'})
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_format_signature = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
        cell_format_header_parent.set_center_across()
        rotate_format.set_center_across()
        rotate_format.set_rotation(90)
        cell_format_header_yellow.set_center_across()
        
        row = 6
        col = 0
        task_types_obj = self.env['ertrac.project.task.type']
        if report_type in ['report_1', 'report_2', 'report_3', 'report_4']:
            col, row, worksheet = self.get_header_row(report_type, col, row, worksheet, cell_format_header_parent)
            col += 1
            row += 2
            row, worksheet = self.get_details_row(
                report_type, row, worksheet, data, timesheets_ids
                , last_detail_column, cell_format_header_parent, cell_format_row, cell_format_header_yellow)
        if report_type in ['report_6', 'report_7']:
            all_work_types = timesheets_ids.mapped('work_type')
            work_type_list = []
            for t in all_work_types:
                if t and t not in work_type_list:
                    work_type_list.append(t)
            # عرض أنواع العمل
            
            if report_type == 'report_7':
                for year in [data.get('year'), data.get('year2')]:
                    # Draw Header
                    year_task_types_total = 0
                    worksheet.write(row, 0, "م", cell_format_header_parent)
                    worksheet.write(row, 1, "نوع العمل", cell_format_header_parent)
                    for idx, month in enumerate(MONTHS):
                        worksheet.write(row, idx + 2, "%s %s" % (month[1], year), cell_format_header_parent)
                    worksheet.write(row, last_detail_column[0], "إجمالى الإنتاج", cell_format_header_parent)
                    worksheet.write(row, comments_column[0], "الملاحظات", cell_format_header_parent)
                    row += 1
                    task_type_ids = task_types_obj.browse(data.get('task_type_ids'))
                    for idx, task_type_id in enumerate(task_type_ids):
                        # Collect Data
                        total_task_type = 0
                        task_type_timesheets = timesheets_ids.filtered(lambda l: l.task_type_id == task_type_id)
                        # Draw Details
                        if task_type_timesheets:
                            worksheet.write(row, 0, idx + 1, cell_format_header_parent)
                            worksheet.write(row, 1, task_type_id.name, cell_format_header_parent)
                            
                            for month_idx, month in enumerate(MONTHS):
                                days = calendar.monthrange(int(year), int(month[0]))
                                month_start = fields.Date.today().replace(year=int(year), month=int(month[0]),
                                                                          day=1)
                                month_end = fields.Date.today().replace(year=int(year), month=int(month[0]),
                                                                        day=days[1])
                                month_timesheet = task_type_timesheets.filtered(lambda ts: month_start <= ts.date <= month_end)
                                amount = sum(l.unit_amount for l in month_timesheet)
                                total_task_type += amount
                                worksheet.write(row, month_idx+2, round(amount, 4), cell_format_row)
                            worksheet.write(row, last_detail_column[0], total_task_type, cell_format_row)
                            row += 1
                            year_task_types_total += total_task_type
                    worksheet.merge_range(row, 0, row, last_detail_column[0] - 1, "إجمالى لأعمال عن عام %s" % year, cell_format_header_parent)
                    worksheet.write(row, last_detail_column[0], year_task_types_total, cell_format_header_parent)
                    row += 2
            if report_type == 'report_6':
                if not data.get('task_type_ids'):
                    raise Warning(_("no records found for your work types"))
                task_type_ids = task_types_obj.browse(data.get('task_type_ids'))
                for idx, task_type_id in enumerate(task_type_ids):
                    # Collect Data
                    task_type_timesheets = timesheets_ids.filtered(lambda l: l.task_type_id == task_type_id)
                    if task_type_timesheets:
                        total_task_type = 0
                        machines_list = []
                        all_machines = task_type_timesheets.mapped('machine')
                        for m in all_machines:
                            if m and m not in machines_list:
                                machines_list.append(m)
                        # if machines_list:
                        # Draw Headers
                        worksheet.merge_range(row, 0, row, comments_column[0], "%s %s"
                                              % (ORDER_LIST[idx], task_type_id.name), cell_format_header_parent)
                        row += 1
                        worksheet.merge_range(row, 0, row+1, 0, "م", cell_format_header_parent)
                        worksheet.merge_range(row, 1, row+1, 1, "رقم المـاكـينه", cell_format_header_parent)
                        worksheet.merge_range(row, last_detail_column[0], row+1, last_detail_column[0],
                                              "إجمالى الإنتاج", cell_format_header_parent)
                        worksheet.merge_range(row, comments_column[0], row + 1, comments_column[0],
                                              "فترات التوقف", cell_format_header_parent)
                        
                        worksheet.merge_range(row, 2, row, last_detail_column[0]-1, "الـشهر", cell_format_header_parent)
                        for idx, month in enumerate(MONTHS):
                            worksheet.write(row + 1, idx+2, "%s %s" % (month[1], data.get('year')), cell_format_header_parent)
                        row += 2
                        # Draw Details
                        for m_idx, machine in enumerate(machines_list):
                            worksheet.write(row, 0, m_idx+1, cell_format_row)
                            worksheet.write(row, 1, machine, cell_format_row)
                            total_machine = 0
                            for month_idx, month in enumerate(MONTHS):
                                days = calendar.monthrange(int(data.get('year')), int(month[0]))
                                month_start = fields.Date.today().replace(year=int(data.get('year')), month=int(month[0]), day=1)
                                month_end = fields.Date.today().replace(year=int(data.get('year')), month=int(month[0]), day=days[1])
                                machine_month_timesheet = task_type_timesheets.\
                                    filtered(lambda ts: ts.machine == machine and month_start <= ts.date <= month_end)
                                amount = sum(l.unit_amount for l in machine_month_timesheet)
                                total_machine += amount
                                worksheet.write(row, month_idx+2, round(amount, 4), cell_format_row)
                            worksheet.write(row, last_detail_column[0], total_machine, cell_format_row)
                            row += 1
                            total_task_type += total_machine
                        worksheet.merge_range(row, 0, row, last_detail_column[0] - 1,
                                              "إجمالى %s لعام %s (كم)" % (task_type_id.name, data.get('year')), cell_format_header_parent)
                        worksheet.write(row, last_detail_column[0], total_task_type, cell_format_header_parent)
                        row += 3

        # Footer
        if report_type in ['report_3', 'report_4']:
            row += 2
            worksheet.write(row, 1, "مدير التخطيط والمتابعه", cell_format_signature)
            worksheet.merge_range(row+1, 0, row+1, 1, "م/ خالد رفيق ابراهيم", cell_format_signature)
        row += 4
        worksheet.merge_range(row, 3, row, 8, "يعتمد / ", bold_right)
        row += 1
        worksheet.merge_range(row, 3, row, 8, "رئيس مجلس الاداره والعضو المنتدب ", bold_right)
        row += 1
        worksheet.merge_range(row, 3, row, 8, "مهندس / مصطفى عبداللطيف أبوالمكارم ", bold_right)
    
    def get_header_row(self, header, col, row, worksheet, cell_format_header_parent):
        if header == 'report_1':
            worksheet.merge_range(row, col, row + 1, col, 'م', cell_format_header_parent)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'الخط', cell_format_header_parent)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'ما تم خلال الشهر(عاديه)', cell_format_header_parent)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'ما تم خلال الشهر(نائيه)', cell_format_header_parent)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'إجمالى ما تم خلال الشهر', cell_format_header_parent)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'الـمـلاحـظـات', cell_format_header_parent)
        elif header in ['report_2', 'report_3', 'report_4', 'report_5']:
            worksheet.merge_range(row, col, row + 1, col, 'م', cell_format_header_parent)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'موقع العمل', cell_format_header_parent)
            col += 1
            if header == 'report_2':
                worksheet.merge_range(row, col, row + 1, col, 'المقرر', cell_format_header_parent)
                col += 1
                worksheet.merge_range(row, col, row + 1, col, 'المنفذ خلال الشهر', cell_format_header_parent)
                col += 1
                worksheet.merge_range(row, col, row + 1, col, 'إجمالى المنفذ', cell_format_header_parent)
                col += 1
            elif header in ['report_3', 'report_4', 'report_5']:
                worksheet.merge_range(row, col, row, col+1, 'المقرر', cell_format_header_parent)
                worksheet.write(row+1, col, 'سكك(كم)', cell_format_header_parent)
                worksheet.write(row+1, col+1, 'تفريعات(مفتاح)', cell_format_header_parent)
                col += 2
                worksheet.merge_range(row, col, row, col+1, 'المنفذ خلال الشهر', cell_format_header_parent)
                worksheet.write(row+1, col, 'سكك(كم)', cell_format_header_parent)
                worksheet.write(row+1, col+1, 'تفريعات(مفتاح)', cell_format_header_parent)
                col += 2
                worksheet.merge_range(row, col, row, col + 1, 'إجمالى المنفذ', cell_format_header_parent)
                worksheet.write(row+1, col, 'سكك(كم)', cell_format_header_parent)
                worksheet.write(row+1, col+1, 'تفريعات(مفتاح)', cell_format_header_parent)
                col += 2
            worksheet.merge_range(row, col, row + 1, col, 'الـمـلاحـظـات', cell_format_header_parent)
        
        return col, row, worksheet
    
    def get_details_row(self, header, row, worksheet, data, timesheets_ids
                        , last_detail_column, cell_format_header_parent, cell_format_row, cell_format_header_yellow):
        # collect task types
        task_types_obj = self.env['ertrac.project.task.type']
        task_type_ids = task_types_obj.browse(data.get('task_type_ids'))
        major_total_col1 = major_total_col2 = major_total_col3 = \
            major_total_col4 = major_total_col5 = major_total_col6 = 0.0
        for idx, task_type_id in enumerate(task_type_ids):
            task_type_timesheet_ids = timesheets_ids.filtered(lambda l: l.task_type_id == task_type_id)
            # Collect Projects
            project_ids = self.env['project.project']
            for pr in task_type_timesheet_ids.mapped('project_id'):
                if pr not in project_ids:
                    project_ids += pr
            if project_ids:
                # Type Row
                worksheet.merge_range(row, 0, row, last_detail_column[0], "%s %s"
                                      % (ORDER_LIST[idx], task_type_id.name), cell_format_header_parent)
                row += 1
                # Print Rows
                count = 1
                total_col1 = total_col2 = total_col3 = total_col4 = total_col5 = total_col6 = 0.0
                for project in project_ids:
                    col = 0
                    worksheet.write(row, col, count, cell_format_row)
                    col += 1
                    worksheet.write(row, col, project.name, cell_format_row)
                    col += 1
                    # Get Orders lines
                    project_timesheets = task_type_timesheet_ids.filtered(lambda l: l.project_id == project)
                    order_line_ids = project_timesheets.mapped('so_line')
                    if header in ['report_1', 'report_2', 'report_3', 'report_4', 'report_5']:
                        # Collect Amounts
                        col1 = col2 = col3 = col4 = col5 = col6 = 0
                        aal_value = sum(l.unit_amount for l in project_timesheets)
                        if header == 'report_1':
                            # ----- total Time sheets
                            # عادديه
                            col1 = sum(l.unit_amount for l in project_timesheets.filtered(lambda l: l.region == 'normal'))
                            # نائيه
                            col2 = sum(l.unit_amount for l in project_timesheets.filtered(lambda l: l.region == 'remote'))
                            # total Time sheets
                            col3 = aal_value
                        elif header == 'report_2':
                            # ----- sale order line مقرر
                            col1 = sum(sol.product_uom_qty for sol in order_line_ids)
                            # total Time sheets
                            col2 = aal_value
                            col3 = sum(sol.qty_delivered for sol in order_line_ids)
                        elif header in ['report_3', 'report_4', 'report_5']:
                            # ----- sale order line (QTY)
                            # نوع العمل سكه
                            path_sols = order_line_ids.filtered(lambda l: l.work_type == 'path')
                            branching_sols = order_line_ids.filtered(lambda l: l.work_type == 'branching')
                            path_timesheets = project_timesheets.filtered(lambda l: l.work_type == 'path')
                            branching_timesheets = project_timesheets.filtered(
                                lambda l: l.work_type == 'branching')
                            if header == 'report_3':
                                # القرير الصيفي
                                path_sols = path_sols.filtered(lambda l: l.season_type == 'summer')
                                branching_sols = branching_sols.filtered(lambda l: l.season_type == 'summer')
                                path_timesheets = path_timesheets.filtered(lambda l: l.season_type == 'summer')
                                branching_timesheets = branching_timesheets.filtered(lambda l: l.season_type == 'summer')
                            elif header == 'report_5':
                                # القرير الشتوي
                                path_sols = path_sols.filtered(lambda l: l.season_type == 'winter')
                                branching_sols = branching_sols.filtered(lambda l: l.season_type == 'winter')
                                path_timesheets = path_timesheets.filtered(lambda l: l.season_type == 'winter')
                                branching_timesheets = branching_timesheets.filtered(lambda l: l.season_type == 'winter')
                            col1 = sum(sol.product_uom_qty for sol in path_sols)
                            # نوع العمل تفريعه
                            col2 = sum(sol.product_uom_qty for sol in branching_sols)
                            # total Time sheets
                            # نوع العمل سكه
                            col3 = sum(l.unit_amount for l in path_timesheets)
                            # نوع العمل تفريعه
                            col4 = sum(l.unit_amount for l in branching_timesheets)
                            # ----- sale order line (QTY)
                            # نوع العمل سكه
                            col5 = sum(sol.qty_delivered for sol in path_sols)
                            # نوع العمل تفريعه
                            col6 = sum(sol.qty_delivered for sol in branching_sols)
                        # Collect Totals
                        total_col1 += col1
                        total_col2 += col2
                        total_col3 += col3
                        total_col4 += col4
                        total_col5 += col5
                        total_col6 += col6
                        # Write Data
                        worksheet.write(row, col, round(col1, 4), cell_format_row)
                        col += 1
                        worksheet.write(row, col, round(col2, 4), cell_format_row)
                        col += 1
                        worksheet.write(row, col, round(col3, 4), cell_format_row)
                        col += 1
                        if header in ['report_3', 'report_4', 'report_5']:
                            worksheet.write(row, col, round(col4, 4), cell_format_row)
                            col += 1
                            worksheet.write(row, col, round(col5, 4), cell_format_row)
                            col += 1
                            worksheet.write(row, col, round(col6, 4), cell_format_row)
                            col += 1
                        row += 1
                        count += 1
                worksheet.merge_range(row, 0, row, 1, 'إجـمـالـى (كم)', cell_format_header_yellow)
                worksheet.write(row, 2, round(total_col1, 4), cell_format_header_yellow)
                worksheet.write(row, 3, round(total_col2, 4), cell_format_header_yellow)
                worksheet.write(row, 4, round(total_col3, 4), cell_format_header_yellow)
                if header in ['report_3', 'report_4', 'report_5']:
                    worksheet.write(row, 5, round(total_col4, 4), cell_format_header_yellow)
                    worksheet.write(row, 6, round(total_col5, 4), cell_format_header_yellow)
                    worksheet.write(row, 7, round(total_col6, 4), cell_format_header_yellow)
                major_total_col1 += total_col1
                major_total_col2 += total_col2
                major_total_col3 += total_col3
                if header in ['report_3', 'report_4']:
                    major_total_col4 += total_col4
                    major_total_col5 += total_col5
                    major_total_col6 += total_col6
                row += 1
        if header in ['report_1', 'report_2', 'report_3', 'report_4', 'report_5']:
            worksheet.merge_range(row, 0, row, 1, 'الإجـمـالـى', cell_format_header_parent)
            worksheet.write(row, 2, round(major_total_col1, 4), cell_format_header_parent)
            worksheet.write(row, 3, round(major_total_col2, 4), cell_format_header_parent)
            worksheet.write(row, 4, round(major_total_col3, 4), cell_format_header_parent)
            if header in ['report_3', 'report_4', 'report_5']:
                worksheet.write(row, 5, round(major_total_col4, 4), cell_format_header_parent)
                worksheet.write(row, 6, round(major_total_col5, 4), cell_format_header_parent)
                worksheet.write(row, 7, round(major_total_col6, 4), cell_format_header_parent)
            row += 1
            percentage1 = percentage2 = 0.0
            
            if header in ['report_1', 'report_2']:
                worksheet.merge_range(row, 0, row, 2, 'نسبه الأعمال المنفذه', cell_format_header_parent)
                if major_total_col1:
                    percentage1 = (major_total_col3 / major_total_col1) * 100
                worksheet.write(row, 3, str(round(percentage1, 4)) + "%", cell_format_header_parent)
                row += 1
                worksheet.merge_range(row, 0, row, 2, 'النسبه المقرره لنهو الاعمال', cell_format_header_parent)
                worksheet.write(row, 3, "100%", cell_format_header_parent)
            elif header in ['report_3', 'report_4', 'report_5']:
                worksheet.merge_range(row, 4, row, 5, 'نسبه الأعمال المنفذه', cell_format_header_parent)
                if major_total_col1:
                    percentage1 = (major_total_col5 / major_total_col1) * 100
                if major_total_col2:
                    percentage2 = (major_total_col6 / major_total_col2) * 100
                worksheet.write(row, 6, str(round(percentage1, 4)) + "%", cell_format_header_parent)
                worksheet.write(row, 7, str(round(percentage2, 4)) + "%", cell_format_header_parent)
                row += 1
                worksheet.merge_range(row, 4, row, 5, 'النسبه المقرره لنهو الاعمال', cell_format_header_parent)
                worksheet.write(row, 6, "100%", cell_format_header_parent)
                worksheet.write(row, 7, "100%", cell_format_header_parent)
        return row, worksheet
# Ahmed Salama Code End.
