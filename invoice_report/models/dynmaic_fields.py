from odoo import models, fields, api


class AcountMove(models.Model):
    _inherit = 'account.move'
    
    contract = fields.Char(string='العقد')
    current = fields.Char(string='جاري')
    # Sector 1
    total_line = fields.Float(string='ضمان اعمال', compute='_compute_total')
    ten_perc = fields.Float(string='10% خصم ضمان الاعمال', compute='_compute_total')
    pure = fields.Float(string='صافي ضمان اعمال', compute='_compute_total')
    # Sector 2
    total_machine_rent = fields.Float(string='خصم إيجار الماكينات', compute='_compute_total')
    # Sector 3
    pure_amount = fields.Float(string='صافي المستخلص', compute='_compute_total')
    
    @api.onchange('invoice_line_ids')
    @api.depends('invoice_line_ids.price_subtotal')
    def _compute_total(self):
        for invoice in self:
            total_line = 0
            products_end = 0
            machine_rent_start = 0
            total_machine_rent = 0
            invoice_lines = invoice.invoice_line_ids
            # Getting IDX of sectors
            for idx, line in enumerate(invoice_lines):
                # print("Line name", line.name)
                if line.name == 'خصم ضمان اعمال':
                    products_end = idx
                if line.name == 'خصم ايجار ماكينات':
                    machine_rent_start = idx + 1
            # print("Last line of sector 1: ", products_end)
            # print("First line of sector 2: ", machine_rent_start)

            # Sector 1  ضمان اعمال
            if products_end:
                for idx, line in enumerate(invoice_lines):
                    if idx == products_end:
                        break
                    total_line += line.price_subtotal
            invoice.total_line = total_line
            invoice.ten_perc = total_line * 0.10
            invoice.pure = total_line - invoice.ten_perc
            # print("Total Sector 1: ", invoice.pure)
            # Sector 2  ايجار الماكينات
            for idx, line in enumerate(invoice_lines):
                if idx >= machine_rent_start:
                    total_machine_rent += line.price_subtotal
            invoice.total_machine_rent = total_machine_rent
            # print("Total Sector 2: ", invoice.total_machine_rent)
            # Sector 3  صافي المستخلص
            invoice.pure_amount = invoice.pure + invoice.total_machine_rent
            # print("Total Sector 3: ", invoice.pure_amount)
        
        
            
            
            





