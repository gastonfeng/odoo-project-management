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
from odoo import models, fields


class purchase_order(models.Model):
    
    _inherit = "purchase.order"

    project_id = fields.Many2one('project.project', 'Project',
                                 states={'confirmed': [('readonly', True)], 'approved': [('readonly', True)],
                                         'done': [('readonly', True)]})
    project_manager = fields.Many2one(related='project_id.user_id', readonly=True, string='Project Manager',
                                      type='many2one', relation="res.users", store=True)

    def onchange_project_id(self, ids, project_id):

        analytic_account_id = ''
        
        if project_id:            
            project_obj = self.pool.get('project.project')
            #Read the project's analytic account
            analytic_account_id = project_obj.read(project_id, 'analytic_account_id')['analytic_account_id']
            
        lines=self.pool.get('purchase.order.line')

        for po in self.browse(ids, context=None):
        #Get the order lines       
            for line in po.order_line:
                lines.write(line.id, {
                        'account_analytic_id': analytic_account_id,                                                              
                })
                                    
        return {}
