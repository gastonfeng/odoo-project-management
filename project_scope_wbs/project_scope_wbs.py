# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Eficent <contact@eficent.com>
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
from odoo import models, fields, api


class task(models.Model):
    _inherit = 'project.task'

    def _project_complete_wbs_name(self, ids, prop, unknow_none, unknow_dict):

        if not ids:
            return []

        res = []

        data_project = []

        project_obj = self.env.get('project.project')

        tasks = self.browse(ids)

        for task in tasks:
            if task.project_id:
                task_project_id = task.project_id.id
                data_project = project_obj.read(task_project_id, ['complete_wbs_name'])
            if data_project:
                res.append((task.id, data_project['complete_wbs_name']))
            else:
                res.append((task.id, ''))
        return dict(res)

    def _project_complete_wbs_code(self, ids, prop, unknow_none, unknow_dict):

        if not ids:
            return []

        res = []

        data_project = []

        project_obj = self.env.get('project.project')

        tasks = self.browse(ids)

        for task in tasks:
            if task.project_id:
                task_project_id = task.project_id.id
                data_project = project_obj.read(task_project_id, ['complete_wbs_code'])
            if data_project:
                res.append((task.id, data_project['complete_wbs_code']))
            else:
                res.append((task.id, ''))
        return dict(res)

    project_complete_wbs_name = fields.Char(compute='_project_complete_wbs_name', type='char',
                                            string='WBS path name', size=250, help='Project Complete WBS path name',
                                            store=True)
    project_complete_wbs_code = fields.Char(compute='_project_complete_wbs_code', type='char', string='WBS path code',
                                            size=250, help='Project Complete WBS path code', store=True)


task()


class account_analytic_account(models.Model):
    _inherit = 'account.analytic.account'

    def get_child_accounts(self, ids):
        result = {}
        read_data = []
        read_data = self.env.get('account.analytic.account').read(ids, ['child_ids'])
        for data in read_data:
            for curr_id in ids:
                result[curr_id] = True
            for child_id in data['child_ids']:
                lchild_id = []
                lchild_id.append(child_id)
                result.update(self.get_child_accounts(lchild_id))
        return result

    def _complete_wbs_code_calc(self, ids, prop, unknow_none, unknow_dict):
        if not ids:
            return []
        res = []
        for account in self.browse(ids):
            data = []
            acc = account
            while acc:
                if acc.code:
                    data.insert(0, acc.code)
                else:
                    data.insert(0, '')
                acc = acc.parent_id

            data = ' / '.join(data)
            res.append((account.id, data))
        return dict(res)

    def _complete_wbs_name_calc(self, ids, prop, unknow_none, unknow_dict):
        if not ids:
            return []
        res = []
        for account in self.browse(ids):
            data = []
            acc = account
            while acc:
                if acc.name:
                    data.insert(0, acc.name)
                else:
                    data.insert(0, '')
                acc = acc.parent_id

            data = ' / '.join(data)
            res.append((account.id, data))
        return dict(res)

    complete_wbs_code = fields.Char(compute='_complete_wbs_code_calc', type='char', string='Full WBS Code', size=250,
                                    help='The full WBS code describes the full path of this component within the project WBS hierarchy',
                                    store=True)
    complete_wbs_name = fields.Char(compute='_complete_wbs_name_calc', type='char', string='Full WBS path',
                                    size=250, help='Full path in the WBS hierarchy',
                                    store=True)
    class_ = fields.Selection(
        [('project', 'Project'), ('subproject', 'Subproject'), ('phase', 'Phase'), ('deliverable', 'Deliverable'),
         ('work_package', 'Work Package')], 'Class',
        help='The classification allows you to create a proper project Work Breakdown Structure')
    lifecycle_stage = fields.Many2one('project.lifecycle', 'Lifecycle Stage')
    child_projects = fields.One2many('project.project', 'parent_id', 'WBS Components')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []

        args = args[:]
        #        if context.get('current_model') == 'project.project':
        #            cr.execute("select analytic_account_id from project_project ")
        #            project_ids = [x[0] for x in cr.fetchall()]
        #            # We cannot return here with normal project_ids, the following process also has to be followed.
        #            # The search should consider the name inhere, earlier it was just bypassing it.
        #            # Hence, we added the args and let the below mentioned procedure do the trick
        #            # Let the search method manage this.
        #            args += [('id', 'in', project_ids)]
        #            return self.name_get( project_ids, context=context)
        accountbycode = self.search([('complete_wbs_code', 'ilike', '%%%s%%' % name)] + args, limit=limit)
        accountbyname = self.search([('complete_wbs_name', 'ilike', '%%%s%%' % name)] + args, limit=limit)
        account = accountbycode + accountbyname

        return account.name_get()

    def code_get(self, ids):
        if not ids:
            return []
        res = []
        for account in self.browse(ids):
            data = []
            acc = account
            while acc:
                if acc.code:
                    data.insert(0, acc.code)
                else:
                    data.insert(0, '')

                acc = acc.parent_id
            data = ' / '.join(data)
            res.append((account.id, data))
        return res

    @api.multi
    def name_get(self):
        res = []
        for account in self:
            data = []
            acc = account
            while acc:
                data.insert(0, acc.name)
                acc = acc.parent_id
            data = ' / '.join(data)
            res2 = self.code_get([account.id])
            if res2:
                data = '[' + res2[0][1] + '] ' + data
                # if project.partner_id.name:
            #    data = data + ' ('+ project.partner_id.name + ')'

            res.append((account.id, data))
        return res


account_analytic_account()


class project(models.Model):
    _name = "project.project"
    _inherit = "project.project"

    def name_get(self, ids):
        if not ids:
            return []
        res = []
        for project in self.browse(ids):
            data = []
            proj = project
            while proj:
                if proj and proj.name:
                    data.insert(0, proj.name)
                else:
                    data.insert(0, '')

                proj = proj.parent_id
            data = ' / '.join(data)
            res2 = self.code_get([project.id])
            if res2:
                data = '[' + res2[0][1] + '] ' + data
                # if project.partner_id.name:
            #    data = data + ' ('+ project.partner_id.name + ')'

            res.append((project.id, data))
        return res

    def code_get(self, ids):
        if not ids:
            return []
        res = []
        for project in self.browse(ids):
            data = []
            proj = project
            while proj:
                if proj.code:
                    data.insert(0, proj.code)
                else:
                    data.insert(0, '')

                proj = proj.parent_id
            data = ' / '.join(data)
            res.append((project.id, data))
        return res

    def _child_compute(self, ids, name, arg):
        result = {}
        project_child_ids = []
        for project in self.browse(ids):
            for child in project.child_ids:
                project_child_list = self.search([('analytic_account_id', '=', child.id)])
                for project_child_id in project_child_list:
                    project_child_ids.append(project_child_id)

            result[project.id] = project_child_ids

        return result

    project_child_complete_ids = fields.Char(compute='_child_compute', relation='project.project',
                                             string="Project Hierarchy", type='many2many')
    parent_id=fields.Many2one('account.analytic.account',string='account')

    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        args = args[:]
        #        if context.get('current_model') == 'project.project':
        #            cr.execute("select analytic_account_id from project_project ")
        #            project_ids = [x[0] for x in cr.fetchall()]
        #            # We cannot return here with normal project_ids, the following process also has to be followed.
        #            # The search should consider the name inhere, earlier it was just bypassing it.
        #            # Hence, we added the args and let the below mentioned procedure do the trick
        #            # Let the search method manage this.
        #            args += [('id', 'in', project_ids)]
        #            return self.name_get( project_ids, context=context)
        projectbycode = self.search([('complete_wbs_code', 'ilike', '%%%s%%' % name)] + args, limit=limit)
        projectbyname = self.search([('complete_wbs_name', 'ilike', '%%%s%%' % name)] + args, limit=limit)
        project = list(set(projectbycode + projectbyname))

        #            newproj = project
        #            while newproj:
        #                newproj = self.search( [('parent_id', 'in', newproj)]+args, limit=limit, context=context)
        #                project += newproj

        return self.name_get(project)


project()
