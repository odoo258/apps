# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import base64
import xlrd
import csv
import cStringIO


class StockInventory(models.TransientModel):
    _name = 'stock.inventory.wizard'

    @api.model
    def _default_location_id(self):
        company_user = self.env.user.company_id
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', company_user.id)], limit=1)
        if warehouse:
            return warehouse.lot_stock_id.id
        else:
            raise UserError(_('You must define a warehouse for the company: %s.') % (company_user.name,))

    inventory_name = fields.Char(string="Inventory Name", required=True)
    location = fields.Many2one(
        'stock.location', string="Location", default=_default_location_id)
    Select_xls_csv = fields.Selection([('csv file import', 'CSV File'),
                                       ('xls file import', 'XLS File')], string='Select')
    xls_file = fields.Binary('File', required=True)
    filename = fields.Char('Filename')
    message = fields.Text(readonly=True)
    is_error = fields.Boolean()
    is_validate = fields.Boolean(default=False)

    @api.multi
    def validate_file(self):
        """Validate excel or csv file"""
        filename = str(self.filename)
        self.is_error = False
        self.message = ""
        if not (filename.endswith('xls') or filename.endswith('xlsx') or filename.endswith('csv')):
            self.message += "Please Import only '.xls' or '.xlsx' or '.csv' File."
        elif (filename.endswith('xls') or filename.endswith('xlsx')):
            column_list = ['id', 'quantity']

            wb = xlrd.open_workbook(
                file_contents=base64.decodestring(self.xls_file))
            sheet = wb.sheet_by_index(0)
            row = sheet.row_values(0)
            invalid_cols = []
            import pdb;pdb.set_trace()
            for key in row:
                key = key.encode('ascii', 'ignore')
                if key.lower() not in column_list:
                    invalid_cols.append(key)
            if invalid_cols:
                self.message = "Invalid Column Name %s", ', '.join(
                    invalid_cols)
            if not self.message:
                for i in range(1, sheet.nrows):
                    row = sheet.row_values(i)
                    firstrow = sheet.row_values(0)
                    firstrow = [str(item).lower() for item in firstrow]
                    product_obj = self.env['product.product'].search(
                        [('id', '=', row[firstrow.index('id')])])
                    if not row[firstrow.index('quantity')]:
                        self.message += "Enter Quantity In Your Excel File"
                    if not product_obj:
                        self.message += "Enter Valid Product Id In Your Excel File"
        else:
            column_list = ['id', 'quantity']
            xls_file = base64.b64decode(self.xls_file)
            file_input = cStringIO.StringIO(xls_file)
            file_input.seek(0)
            rows = []
            delimeter = ','
            reader = csv.reader(file_input, delimiter=delimeter,
                                lineterminator='\r\n')
            for row in reader:
                rows.append(row)
            firstrow = [str(item).lower() for item in rows[0]]
            match = [column for column in firstrow if column not in column_list]
            if match:
                self.message += "Enter Valid Column Name"
            if not self.message:
                for row in rows[1:]:
                    rows[0] = [str(item).lower() for item in rows[0]]
                    product_obj = self.env['product.product'].search(
                        [('id', '=', row[rows[0].index('id')])])
                    if not row[rows[0].index('quantity')]:
                        self.message += "Enter Quantity In Your Excel File"
                    if not product_obj:
                        self.message += "Enter Valid Product Id In Your Excel File"

        if self.message:
            self.is_error = True
        if not self.is_error:
            self.is_validate = True
        return {
            'res_id': self.id,
            'view_id': self.env.ref('import_stock_inventory_drc.import_stock_inventory_view_wizard_form').ids,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.inventory.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

    @api.multi
    def read_xls_csv(self):
        """
            Read Excel and CSV file
            Import record in stock inventory line
        """
        filename = str(self.filename)
        location_stock_id = self.location
        vals = []
        inventory_create = self.env['stock.inventory']

        if (filename.endswith('xls') or filename.endswith('xlsx')):
            wb = xlrd.open_workbook(
                file_contents=base64.decodestring(self.xls_file))
            sheet = wb.sheet_by_index(0)

            for i in range(1, sheet.nrows):
                row = sheet.row_values(i)
                firstrow = sheet.row_values(0)
                firstrow = [str(item).lower() for item in firstrow]
                pid = row[firstrow.index('id')]
                quantity = row[firstrow.index('quantity')]
                product_obj = self.env['product.product'].search(
                    [('id', '=', pid)])
                vals.append({
                    'product_code': product_obj.default_code,
                    'product_qty': quantity,
                    'location_id': location_stock_id.id,
                    'product_id': product_obj.id
                })
            inv = inventory_create.create({'name': self.inventory_name,
                                     'location_id': location_stock_id.id,
                                     'filter': 'partial'})
            stock_inventory_line = self.env['stock.inventory.line']
            # inv.prepare_inventory()
            for record in vals:
                record.update({'inventory_id': inv.id})
                stock_inventory_line.create(record)
            inv.action_done()

        else:
            xls_file = base64.b64decode(self.xls_file)
            file_input = cStringIO.StringIO(xls_file)
            file_input.seek(0)
            rows = []
            delimeter = ','
            reader = csv.reader(file_input, delimiter=delimeter,
                                lineterminator='\r\n')
            for row in reader:
                rows.append(row)
            for row in rows[1:]:
                rows[0] = [str(item).lower() for item in rows[0]]
                product_obj = self.env['product.product'].search(
                    [('id', '=', row[rows[0].index('id')])])
                vals.append({
                            'product_code': row[rows[0].index('id')],
                            'product_qty': row[rows[0].index('quantity')],
                            'location_id': location_stock_id.id,
                            'product_id': product_obj.id
                            })
            inv = inventory_create.create({'name': self.inventory_name,
                                     'location_id': location_stock_id.id,
                                     'filter': 'partial'})
            stock_inventory_line = self.env['stock.inventory.line']
            # inv.prepare_inventory()
            for record in vals:
                record.update({'inventory_id': inv.id})
                stock_inventory_line.create(record)
            inv.action_done()
        return {
            'name': 'Stock import',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'res_id': self.id,
            'view_mode': 'tree,form',
            'res_model': 'stock.inventory',
            'target': 'current',
        }
