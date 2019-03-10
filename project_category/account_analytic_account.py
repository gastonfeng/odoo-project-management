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


from odoo import tools

from odoo import models, fields, api


class account_analytic_account(models.Model):
    @api.multi
    def _categories_name_calc(self):

        res = []

        accounts_br = self

        for account in accounts_br:
            data = []
            categories_br = account.category_id
            if categories_br:
                for category_br in categories_br:
                    cat_name = category_br.complete_name or ''
                    data.insert(0, cat_name)
                data.sort(key=None, reverse=False)
                data_str = ', '.join(map(tools.ustr, data))

            else:
                data_str = ''

            res.append((account.id, data_str))

        return dict(res)

    _inherit = 'account.analytic.account'

    category_id = fields.Many2many('analytic.account.category', 'analytic_account_category_rel', 'account_id',
                                   'category_id', 'Categories')
    categories_name_str = fields.Text(compute='_categories_name_calc', method=True, type='text', string='Categories',
                                      help='Analytic account categories')
