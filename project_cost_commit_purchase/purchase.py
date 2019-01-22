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


class purchase_order(models.Model):

    _inherit = 'purchase.order'
    #TODO: implement messages system
    order_line = fields.One2many('purchase.order.line', 'order_id', 'Order Lines',
                                 states={'confirmed': [('readonly', True)], 'approved': [('readonly', True)],
                                         'done': [('readonly', True)]})

    def wkf_confirm_order(self, ids, context=None):
        purch_order_line = self.env.get('purchase.order.line')

        res = super(purchase_order, self).wkf_confirm_order(ids, context)

        for po in self.browse(ids, context=context):
            purch_order_line.create_analytic_lines_commit([line.id for line in po.order_line], context)

        return res

    def wkf_purchase_cancel(self, ids, context=None):

        self.write(ids, {'state': 'cancel'})

        obj_commitment_analytic_line = self.env.get('account.analytic.line.commit')

        for purchase in self.browse(ids, context=context):
            for po_lines in purchase.order_line:
                for ana_lines in po_lines.analytic_lines_commit:
                    obj_commitment_analytic_line.unlink(ana_lines.id)
                      
        return True

    def action_cancel(self, ids, context=None):

        super(purchase_order, self).action_cancel(ids, context)

        obj_commitment_analytic_line = self.env.get('account.analytic.line.commit')

        for purchase in self.browse(ids, context=context):
            for po_lines in purchase.order_line:
                for ana_lines in po_lines.analytic_lines_commit:
                    obj_commitment_analytic_line.unlink(ana_lines.id)
                      
        return True


purchase_order()


class purchase_order_line(models.Model):
    
    _inherit = 'purchase.order.line'     
          
    _columns = {
            'analytic_lines_commit': fields.one2many('account.analytic.line.commit', 'purchase_line_id', 'Commitment Analytic lines'),
    }

    def create_analytic_lines_commit(self, ids, context=None):
        acc_ana_line_obj = self.env.get('account.analytic.line.commit')
        journal_obj = self.env.get('account.analytic.journal.commit')
        journal_id = journal_obj.search([('type', '=', 'purchase')], context=None)
        journal_id = journal_id and journal_id[0] or False
        cur_obj = self.env.get('res.currency')

        for obj_line in self.browse(ids, context=context):
            cur = obj_line.order_id and obj_line.order_id.pricelist_id and obj_line.order_id.pricelist_id.currency_id
            
            if obj_line.account_analytic_id:                
                vals_lines = {
                    'name': obj_line.name,
                    'date': obj_line.order_id and obj_line.order_id.date_order or False,
                    'account_id': obj_line.account_analytic_id and obj_line.account_analytic_id.id or False,
                    'unit_amount': obj_line.product_qty,
                    'product_id': obj_line.product_id and obj_line.product_id.id or False,
                    'product_uom_id': obj_line.product_uom and obj_line.product_uom.id or False,
                    'amount': -1 * obj_line.price_subtotal,
                    'general_account_id': False,
                    'journal_id': journal_id or False,
                    'ref': obj_line.name,                    
                    'user_id': uid,
                    'purchase_line_id': obj_line.id,
                    'currency_id': cur.id,
                    'amount_currency': -1 * cur_obj.round(cur, obj_line.price_subtotal),
                }
                acc_ana_line_obj.create(vals_lines)
        return True

                 
                 
purchase_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: