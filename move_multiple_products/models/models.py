# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import except_orm


class scrap_products_by_quantity(models.Model):
    _name = 'scrap.products.by.quantity'

    name = fields.Char('Name')
    src_location_id = fields.Many2one('stock.location', string='Source Location')
    dest_location_id = fields.Many2one('stock.location', string='Destination Location')
    date = fields.Date('Date')
    scrap_line = fields.One2many('scrap.product.line', 'scrap_id', 'Scrap Product Line')
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Moved')], string='Status', readonly=True, copy=False, select=True)
    _defaults = {'date':datetime.today(),
                 'name': "Draft stock move"}

    @api.model
    def create(self, vals):
        if vals.get('name', 'Draft stock move') == 'Draft stock move':
            vals['name'] = self.env['ir.sequence'].get('scrap.products.by.quantity')
        res = super(scrap_products_by_quantity, self).create(vals)
        res.state = 'draft'
        return res

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        move_obj = self.env['stock.move']
        message = ''
        for line in self.scrap_line:
            quant_obj = self.env['stock.quant'].search([('product_id', '=', line.product_id.id), ('location_id', '=', line.src_loc_id.id)])
            total_qty = 0
            for i in quant_obj:
                total_qty += i.qty

            if line.quantity > total_qty:
                    message += 'Only ' + str(total_qty) + ' ' + str(line.product_uom.name) + '  available for product ' + str(line.product_id.name) + '\n'
        if message:
            res = self.write({'flag': True})
            raise except_orm(('User Error!'), (message))
        move_obj = self.env['stock.move']
        for line in self.scrap_line:
            res = move_obj.create({'product_uom_qty': line.quantity,
                                'product_uom': line.product_uom.id,
                                'location_id': line.src_loc_id.id,
                                'name': line.product_id.name,
                                'location_dest_id': line.dest_loc_id.id,
                                'product_id': line.product_id.id,
                                'origin': self.name})
            res.action_done()
        self.state = 'done'

    @api.multi
    def force_move(self):
        move_obj = self.env['stock.move']
        for line in self.scrap_line:
            res = move_obj.create({'product_uom_qty': line.quantity,
                              'product_uom': line.product_uom.id,
                              'location_id': line.src_loc_id.id,
                              'name': line.product_id.name,
                              'location_dest_id': line.dest_loc_id.id,
                              'product_id': line.product_id.id,
                              'origin': self.name})
            res.action_done()
        self.state = 'done'

    @api.multi
    def unlink(self):
        for scrap in self:
            if scrap.state not in ('draft', 'confirmed'):
                raise except_orm(('User Error!'), ('You can only delete draft and confirmed moves.'))
        return super(scrap_products_by_quantity, self).unlink()

    @api.multi
    def check_quantity(self):
        for line in self.scrap_line:
            if line.quantity == 0:
                return False
            else:
                return True

    _constraints = [(check_quantity, 'Quantity must be greather than 0', ['scrap_line'])]


class scrap_product_line(models.Model):
    _name = 'scrap.product.line'

    scrap_id = fields.Many2one('scrap.product.by.quantity', 'Scrap Reference', required=True, ondelete='cascade', select=True)
    product_id = fields.Many2one('product.product', 'Product Name', ondelete='restrict', domain="[('type','!=','service')]")
    quantity = fields.Float(string='Quanity')
    src_loc_id = fields.Many2one('stock.location', string='Source Location', store=True)
    dest_loc_id = fields.Many2one('stock.location', string="Destination Location")
    product_uom = fields.Many2one('product.uom', related='product_id.uom_id', string='Product Unit of Measure')


    _sql_constraints = [
        ('product_unique', 'unique (product_id, scrap_id)', ' One product can not be allow for multiple time!')
    ]

    
    @api.onchange('product_id')
    def get_quantity(self):
        quant_obj = self.env['stock.quant'].search([('product_id','=',self.product_id.id),('location_id','=', self.src_loc_id.id)])
        total_qty = 0
        for i in quant_obj:
            total_qty += i.qty
        self.quantity = total_qty
        self.available_quantity = total_qty


    



