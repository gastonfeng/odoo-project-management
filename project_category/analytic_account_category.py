# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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
from odoo.osv import osv


class analytic_account_category(models.Model):
    def name_get(self, ids, context=None):
        if not len(ids):
            return []
        reads = self.read(ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args=[]
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search([('name', operator, name)] + args, limit=limit)
        else:
            ids = self.search(args, limit=limit)
        return self.name_get(ids)

    def _name_get_fnc(self, ids, prop, unknow_none, context=None):
        res = self.name_get(ids, context=context)
        return dict(res)

    _description='Analytic account & project Categories'
    _name = 'analytic.account.category'
    name = fields.Char('Category Name', required=True, size=64, translate=True)
    parent_id = fields.Many2one('analytic.account.category', 'Parent Category', index=True, ondelete='cascade')
    complete_name = fields.Char(compute='_name_get_fnc', method=True, type="char", string='Full Name')
    child_ids = fields.One2many('analytic.account.category', 'parent_id', 'Child Categories')
    active = fields.Boolean('Active', help="The active field allows you to hide the category without removing it.")
    parent_left = fields.Integer('Left parent', index=True)
    parent_right = fields.Integer('Right parent', index=True)
    account_ids = fields.Many2many('account.analytic.account', 'analytic_account_category_rel', 'category_id',
                                   'account_id', 'Categories')
    _constraints = [
        (osv.osv._check_recursion, 'Error ! You can not create recursive categories.', ['parent_id'])
    ]
    _defaults = {
        'active' : lambda *a: 1,
    }
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'
    
analytic_account_category()