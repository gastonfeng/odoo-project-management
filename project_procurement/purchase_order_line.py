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


from odoo import netsvc
from odoo.tools.translate import _

from odoo import models, fields
from odoo.osv import osv


class purchase_order_line(models.Model):
    _inherit = "purchase.order.line"

    order_project_id = fields.Many2one(related='order_id.project_id', type='many2one', relation='project.project',
                                       string='Project', readonly=True)

    def create(self, vals, *args, **kwargs):
        if 'order_id' in vals:
            order_obj = self.env.get('purchase.order').browse(vals['order_id'])

        analytic_account_id = ''

        if order_obj.project_id:
            project_obj = self.env.get('project.project')
            # Read the project's analytic account
            analytic_account_id = project_obj.read(order_obj.project_id.id, 'analytic_account_id')[
                'analytic_account_id']
            vals['account_analytic_id'] = analytic_account_id

        return super(purchase_order_line, self).create(vals, *args, **kwargs)

    def button_cancel(self, ids):
        for line in self.browse(ids):
            if line.invoiced:
                raise osv.except_osv(_('Invalid action !'),
                                     _('You cannot cancel a purchase order line that has already been invoiced !'))
            for move_line in line.move_ids:
                if move_line.state != 'cancel':
                    raise osv.except_osv(
                        _('Could not cancel purchase order line!'),
                        _('You must first cancel stock moves attached to this purchase order line.'))
        return self.write(ids, {'state': 'cancel'})

    def button_confirm(self, ids):
        return self.write(ids, {'state': 'confirmed'})

    def button_done(self, ids):
        wf_service = netsvc.LocalService("workflow")
        res = self.write(ids, {'state': 'done'})
        for line in self.browse(ids):
            wf_service.trg_write(self.env.uid, 'purchase.order', line.order_id.id, self._cr)
        return res
