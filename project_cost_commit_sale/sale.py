# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################



#
# Model definition
#
from odoo import models, fields


class sale_order(models.Model):

    _inherit = 'sale.order'
    
    def action_wait(self,  ids, *args):
        sale_order_line = self.pool.get('sale.order.line') 
        
        res = super(sale_order, self).action_wait( ids, args)

        for so in self.browse(ids):
            sale_order_line.create_analytic_lines_commit( [line.id for line in so.order_line], None)

        return res

    def action_cancel(self,  ids, context=None):

        super(sale_order, self).action_cancel( ids, context)
        
        obj_commitment_analytic_line = self.pool.get('account.analytic.line.commit')

        for sale in self.browse(ids):
            for so_lines in sale.order_line:
                for ana_lines in so_lines.analytic_lines_commit:
                    obj_commitment_analytic_line.unlink(ana_lines.id)
                      
        return True




class sale_order_line(models.Model):
    
    _inherit = 'sale.order.line'

    analytic_lines_commit = fields.One2many('account.analytic.line.commit', 'sale_line_id', 'Commitment Analytic lines')

    def create_analytic_lines_commit(self, ids):
        acc_ana_line_obj = self.pool.get('account.analytic.line.commit')
        journal_obj = self.pool.get('account.analytic.journal.commit')
        journal_id = journal_obj.search( [('type', '=', 'sale')], context=None)
        journal_id = journal_id and journal_id[0] or False
        cur_obj=self.pool.get('res.currency')

        for obj_line in self.browse(ids):
            cur = obj_line.order_id and obj_line.order_id.pricelist_id and obj_line.order_id.pricelist_id.currency_id
            
            if obj_line.order_id and obj_line.order_id.project:                
                vals_lines = {
                    'name': obj_line.name,
                    'date': obj_line.order_id and obj_line.order_id.date_order or False,
                    'account_id': obj_line.order_id and obj_line.order_id.project and obj_line.order_id.project.analytic_account_id and obj_line.order_id.project.analytic_account_id.id or False,
                    'unit_amount': obj_line.product_uom_qty,
                    'product_id': obj_line.product_id and obj_line.product_id.id or False,
                    'product_uom_id': obj_line.product_uom and obj_line.product_uom.id or False,
                    'amount': obj_line.price_subtotal,
                    'general_account_id': False,
                    'journal_id': journal_id or False,
                    'ref': obj_line.name,
                    'user_id': self.uid,
                    'sale_line_id': obj_line.id,
                    'currency_id': cur.id,
                    'amount_currency': cur_obj.round( cur, obj_line.price_subtotal),
                }
                acc_ana_line_obj.create( vals_lines)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
