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


from openerp.tools.translate import _

from odoo import models, fields
from odoo.osv import osv


class project(models.Model):
    _name = "project.project"
    _inherit = "project.project"

    predecessor_ids = fields.Many2many('project.project', 'projects_relationships', 'project_id', 'predecessor_id',
                                       'Predecessor Project')
    successor_ids = fields.Many2many('project.project', 'projects_relationships', 'predecessor_id', 'project_id',
                                     'Successor Project')

    def set_restart(self, ids, *args):
        self.write(ids, {'state': 'open'})
        return True

    def set_reopen(self, ids, *args):
        self.write(ids, {'state': 'open'})
        return True

    def set_ready(self, ids, *args):
        self.write(ids, {'state': 'ready'})
        self.send_ready(ids)
        return True

    def send_ready(self, ids):

        project_br = self.browse(ids)
        for p in project_br:
            
            if p.user_id and p.user_id.address_id and p.user_id.address_id.email:
                to_adr = p.user_id.address_id.email
            else:
                raise osv.except_osv(_('Error'), _("Couldn't send mail because the project manager email address is not configured!"))

            email_template_ids = self.env.get('email.template').search(
                [('object_name.name', '=', 'Project'), ('name', '=', 'Project status change')], context=None)
            for email_template_id in email_template_ids:
                self.env.get('email.template').generate_mail(email_template_id, ids, context=None)
                        
            
        return {}

    def set_done(self, ids, *args):

        res = super(project, self).set_done(ids, *args)

        project_obj = self.env.get('project.project')
        projects = self.browse(ids)
        
        for p in projects:
            for successor in p.successor_ids:
                successor_project_br = project_obj.browse(successor.id)
                if successor_project_br.state == 'draft':
                    project_obj.set_ready([successor.id])
                    
        for proj in projects:
            purchase_order_obj = self.env.get('purchase.order')
            purchase_order_ids = purchase_order_obj.search(
                [('project_id', '=', proj.id), ('state', 'not in', ['cancel', 'done', 'approved'])])
            
            if purchase_order_ids:                    
                raise osv.except_osv(_('User Error'), _('You must complete all active purchase orders related to this project before closing it.'))
                            
        return res        

project()

