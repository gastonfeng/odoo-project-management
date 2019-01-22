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


class account_analytic_journal_commit(models.Model):
    
    _name = 'account.analytic.journal.commit'
    _description = 'Analytic Journal Commitments'

    name = fields.Char('Commitments Journal Name', size=64, required=True)
    code = fields.Char('Commitments Journal Code', size=8)
    active = fields.Boolean('Active',
                            help="If the active field is set to False, it will allow you to hide the analytic journal without removing it.")
    type = fields.Selection([('sale', 'Sale'), ('purchase', 'Purchase'), ('cash', 'Cash'), ('general', 'General'),
                             ('situation', 'Situation')], 'Type', size=32, required=True,
                            help="Gives the type of the analytic journal. When it needs for a document (eg: an invoice) to create analytic entries, OpenERP will look for a matching journal of the same type.")
    line_ids = fields.One2many('account.analytic.line.commit', 'journal_id', 'Lines')
    company_id = fields.Many2one('res.company', 'Company', required=True)
    analytic_journal = fields.Many2one('account.analytic.journal', 'Actual Analytic journal', required=False)

    _defaults = {
        'active': True,
        'type': 'general',
        'company_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
    }


