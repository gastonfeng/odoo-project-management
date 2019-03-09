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

import time

#
# Use period and Journal for selection or resources
#
class account_analytic_journal_plan(object):
    def __init__(self,  name, context):
        super(account_analytic_journal_plan, self).__init__( name, context=context)
        self.localcontext.update( {
            'time': time,
            'lines': self._lines,
            'lines_a': self._lines_a,
            'sum_general': self._sum_general,
            'sum_analytic': self._sum_analytic,
        })

    def _lines(self, journal_id, date1, date2):
        self.cr.execute('SELECT DISTINCT move_id FROM account_analytic_line_plan WHERE (date>=%s) AND (date<=%s) AND (journal_id=%s) AND (move_id is not null)', (date1, date2, journal_id,))
        ids = map(lambda x: x[0], self.cr.fetchall())
        return self.pool.get('account.move.line').browse(self.cr, self.uid, ids)

    def _lines_a(self, move_id, journal_id, date1, date2):
        ids = self.pool.get('account.analytic.line.plan').search(self.cr, self.uid, [('move_id','=',move_id), ('journal_id','=',journal_id), ('date','>=',date1), ('date','<=',date2)])
        if not ids:
            return []
        return self.pool.get('account.analytic.line.plan').browse(self.cr, self.uid, ids)
        
    def _sum_general(self, journal_id, date1, date2):
        self.cr.execute('SELECT SUM(debit-credit) FROM account_move_line WHERE id IN (SELECT move_id FROM account_analytic_line_plan WHERE (date>=%s) AND (date<=%s) AND (journal_id=%s) AND (move_id is not null))', (date1, date2, journal_id,))
        return self.cr.fetchall()[0][0] or 0

    def _sum_analytic(self, journal_id, date1, date2):
        self.cr.execute("SELECT SUM(amount) FROM account_analytic_line_plan WHERE date>=%s AND date<=%s AND journal_id=%s", (date1, date2, journal_id))
        res = self.cr.dictfetchone()
        return res['sum'] or 0

# report_sxw.report_sxw('report.account.analytic.journal.plan', 'account.analytic.journal.plan', 'addons/project_cost/report/account_analytic_journal_plan.rml',parser=account_analytic_journal_plan,header="internal")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

