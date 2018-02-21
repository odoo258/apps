# -*- coding: utf-8 -*-
import odoo
from odoo.tests.common import TransactionCase
@odoo.tests.common.post_install(True)
@odoo.tests.common.at_install(False)

class TestMove(TransactionCase):

    def test_move(self):
        scrap_obj = self.env['scrap.products.by.quantity']
        scrap_lines_obj = self.env['scrap.product.line']
        product_obj = self.env['product.product']
        stock_move_obj = self.env['stock.move']
        location_obj = self.env['stock.location']

        src_location = location_obj.create({'name': 'Source Location'})
        dest_location = location_obj.create({'name': 'Destination Location'})
        product = product_obj.create({'name': 'Test Product'})
        scrap = scrap_obj.create({'src_location_id': src_location.id, 'dest_location_id': dest_location.id})
        line = scrap_lines_obj.create({'product_id': product.id, 'quantity': 5, 'src_loc_id': src_location.id, 'dest_loc_id': dest_location.id, 'product_uom': product.uom_id.id, 'scrap_id': scrap.id})
        scrap.state = 'confirmed'
        for line in scrap.scrap_line:
            res = stock_move_obj.create({'product_uom_qty': line.quantity,
                              'product_uom': line.product_uom.id,
                              'location_id': line.src_loc_id.id,
                              'name': line.product_id.name,
                              'location_dest_id': line.dest_loc_id.id,
                              'product_id': line.product_id.id,
                              'origin': scrap.name})
            res.action_done()
        scrap.state = 'done'
