# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import osv, fields

class project_progress(osv.osv_memory):
    _name = 'project.progress'
    _description = 'Project Progress'

    show_milestones = fields.Boolean('Milestones', help='Show milestones')
    show_tasks = fields.Boolean('Tasks', help='Show tasks')
    show_meetings = fields.Boolean('Meetings', help='Show meetings')
    show_issues = fields.Boolean('Issues', help='Show issues')

    _defaults = {
        'show_milestones':True,
        'show_tasks':True,
        'show_meetings':True,
        'show_issues':True,        
    }

    def check_report(self,  ids, context=None):
        datas = {}
        if context is None:
            context = {}
        data = self.read( ids)[0]
        datas = {
             'ids': context.get('active_ids',[]),
             'model': 'project.project',
             'form': data
                 }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'project.progress',
            'datas': datas,
            }

project_progress()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

