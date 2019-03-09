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

import operator
import time


# from openerp.report import report_sxw

#
# Use period and Journal for selection or resources
#
class account_analytic_balance_plan(object):
    def __init__(self, name, context):
        super(account_analytic_balance_plan, self).__init__(name, context=context)
        self.localcontext.update({
            'time': time,
            'get_objects': self._get_objects,
            'move_sum': self._move_sum,
            'sum_all': self._sum_all,
            'sum_balance': self._sum_balance,
            'move_sum_balance': self._move_sum_balance,

            'move_sum_plan': self._move_sum_plan,
            'sum_all_plan': self._sum_all_plan,
            'sum_balance_plan': self._sum_balance_plan,
            'move_sum_balance_plan': self._move_sum_balance_plan,

            'move_sum_commit': self._move_sum_commit,
            'sum_all_commit': self._sum_all_commit,
            'sum_balance_commit': self._sum_balance_commit,
            'move_sum_balance_commit': self._move_sum_balance_commit,

            'move_sum_budget': self._move_sum_budget,
            'sum_all_budget': self._sum_all_budget,
            'sum_balance_budget': self._sum_balance_budget,
            'move_sum_balance_budget': self._move_sum_balance_budget,
        })
        self.acc_ids = []
        self.read_data = []
        self.empty_acc = False
        self.acc_data_dict = {}  # maintains a relation with an account with its successors.
        self.acc_data_dict_plan = {}  # maintains a relation with an account with its successors.
        self.acc_data_dict_commit = {}  # maintains a relation with an account with its successors.
        self.acc_data_dict_budget = {}  # maintains a relation with an account with its successors.
        self.acc_sum_list = []  # maintains a list of all ids
        self.acc_sum_list_plan = []  # maintains a list of all ids
        self.acc_sum_list_commit = []  # maintains a list of all ids
        self.acc_sum_list_budget = []  # maintains a list of all ids

    def get_children(self, ids):
        read_data = self.pool.get('account.analytic.account').read(self.cr, self.uid, ids,
                                                                   ['child_ids', 'complete_wbs_code',
                                                                    'complete_wbs_name', 'balance', 'balance_plan',
                                                                    'balance_commit', 'date_start', 'date', 'state'])
        for data in read_data:
            if (data['id'] not in self.acc_ids):
                inculde_empty = True
                if (not self.empty_acc) and (
                        data['balance'] == 0.00 and data['balance_plan'] == 0.00 and data['balance_commit'] == 0.00):
                    inculde_empty = False
                if inculde_empty:
                    self.acc_ids.append(data['id'])
                    self.read_data.append(data)
                    if data['child_ids']:
                        self.get_children(data['child_ids'])
        return True

    def _get_objects(self, empty_acc):
        if self.read_data:
            return self.read_data
        self.empty_acc = empty_acc
        self.read_data = []
        self.get_children(self.ids)
        get_key = operator.attrgetter('complete_wbs_code')
        read_data_sorted = sorted(self.read_data, key=lambda mbr: get_key(mbr).lower(), reverse=False)
        return read_data_sorted

    def _move_sum(self, account_id, date1, date2, option):
        if account_id not in self.acc_data_dict:
            account_analytic_obj = self.pool.get('account.analytic.account')
            ids = account_analytic_obj.search(self.cr, self.uid, [('parent_id', 'child_of', [account_id])])
            self.acc_data_dict[account_id] = ids
        else:
            ids = self.acc_data_dict[account_id]

        query_params = (tuple(ids), date1, date2)
        if option == "credit":
            self.cr.execute("SELECT COALESCE(-sum(amount),0.0) FROM account_analytic_line \
                    WHERE account_id IN %s AND date>=%s AND date<=%s AND amount<0", query_params)
        elif option == "debit":
            self.cr.execute("SELECT COALESCE(sum(amount),0.0) FROM account_analytic_line \
                    WHERE account_id IN %s\
                        AND date>=%s AND date<=%s AND amount>0", query_params)
        elif option == "quantity":
            self.cr.execute("SELECT COALESCE(sum(unit_amount),0.0) FROM account_analytic_line \
                WHERE account_id IN %s\
                    AND date>=%s AND date<=%s", query_params)

        return self.cr.fetchone()[0] or 0.0

    def _move_sum_plan(self, account_id, date1, date2, option):
        if account_id not in self.acc_data_dict_plan:
            account_analytic_obj = self.pool.get('account.analytic.account')
            ids = account_analytic_obj.search(self.cr, self.uid, [('parent_id', 'child_of', [account_id])])
            self.acc_data_dict_plan[account_id] = ids
        else:
            ids = self.acc_data_dict_plan[account_id]

        query_params = (tuple(ids), date1, date2)
        if option == "credit_plan":
            self.cr.execute("SELECT COALESCE(-sum(amount),0.0) FROM account_analytic_line_plan \
                    WHERE account_id IN %s AND date>=%s AND date<=%s AND amount<0", query_params)
        elif option == "debit_plan":
            self.cr.execute("SELECT COALESCE(sum(amount),0.0) FROM account_analytic_line_plan \
                    WHERE account_id IN %s\
                        AND date>=%s AND date<=%s AND amount>0", query_params)
        elif option == "quantity_plan":
            self.cr.execute("SELECT COALESCE(sum(unit_amount),0.0) FROM account_analytic_line_plan \
                WHERE account_id IN %s\
                    AND date>=%s AND date<=%s", query_params)

        return self.cr.fetchone()[0] or 0.0

    def _move_sum_commit(self, account_id, date1, date2, option):
        if account_id not in self.acc_data_dict_commit:
            account_analytic_obj = self.pool.get('account.analytic.account')
            ids = account_analytic_obj.search(self.cr, self.uid, [('parent_id', 'child_of', [account_id])])
            self.acc_data_dict_commit[account_id] = ids
        else:
            ids = self.acc_data_dict_commit[account_id]

        query_params = (tuple(ids), date1, date2)
        if option == "credit_commit":
            self.cr.execute("SELECT COALESCE(-sum(amount),0.0) FROM account_analytic_line_commit \
                    WHERE account_id IN %s AND date>=%s AND date<=%s AND amount<0", query_params)
        elif option == "debit_commit":
            self.cr.execute("SELECT COALESCE(sum(amount),0.0) FROM account_analytic_line_commit \
                    WHERE account_id IN %s\
                        AND date>=%s AND date<=%s AND amount>0", query_params)
        elif option == "quantity_commit":
            self.cr.execute("SELECT COALESCE(sum(unit_amount),0.0) FROM account_analytic_line_commit \
                WHERE account_id IN %s\
                    AND date>=%s AND date<=%s", query_params)

        return self.cr.fetchone()[0] or 0.0

    def _move_sum_budget(self, account_id, date1, date2, crossovered_budget_id, option):
        if not crossovered_budget_id:
            return 0.0
        if account_id not in self.acc_data_dict_budget:
            account_analytic_obj = self.pool.get('account.analytic.account')
            ids = account_analytic_obj.search(self.cr, self.uid, [('parent_id', 'child_of', [account_id])])
            self.acc_data_dict_budget[account_id] = ids
        else:
            ids = self.acc_data_dict_budget[account_id]

        query_params = (tuple(ids), date1, date2, crossovered_budget_id)
        if option == "credit_budget":
            self.cr.execute("SELECT COALESCE(-sum(planned_amount),0.0) \
                    FROM crossovered_budget_lines \
                    WHERE (analytic_account_id IN %s) \
                    AND (date_from<=%s) \
                    AND (date_to>=%s) \
                    AND (planned_amount<0) \
                    AND (crossovered_budget_id=%s)", query_params)
        elif option == "debit_budget":
            self.cr.execute("SELECT COALESCE(sum(planned_amount),0.0) \
                    FROM crossovered_budget_lines \
                    WHERE (analytic_account_id IN %s) \
                    AND (date_from<=%s) \
                    AND (date_to>=%s) \
                    AND (planned_amount>0) \
                    AND (crossovered_budget_id=%s)", query_params)

        return self.cr.fetchone()[0] or 0.0

    def _move_sum_balance(self, account_id, date1, date2):
        debit = self._move_sum(account_id, date1, date2, 'debit')
        credit = self._move_sum(account_id, date1, date2, 'credit')
        return (debit - credit)

    def _move_sum_balance_plan(self, account_id, date1, date2):
        debit = self._move_sum_plan(account_id, date1, date2, 'debit_plan')
        credit = self._move_sum_plan(account_id, date1, date2, 'credit_plan')
        return (debit - credit)

    def _move_sum_balance_commit(self, account_id, date1, date2):
        debit = self._move_sum_commit(account_id, date1, date2, 'debit_commit')
        credit = self._move_sum_commit(account_id, date1, date2, 'credit_commit')
        return (debit - credit)

    def _move_sum_balance_budget(self, account_id, date1, date2, crossovered_budget_id):
        debit = self._move_sum_budget(account_id, date1, date2, crossovered_budget_id, 'debit_budget')
        credit = self._move_sum_budget(account_id, date1, date2, crossovered_budget_id, 'credit_budget')
        return (debit - credit)

    def _sum_all_budget(self, accounts, date1, date2, crossovered_budget_id, option):
        account_analytic_obj = self.pool.get('account.analytic.account')
        ids = map(lambda x: x['id'], accounts)
        if not crossovered_budget_id:
            return 0.0
        if not ids:
            return 0.0

        if not self.acc_sum_list_budget:
            ids2 = account_analytic_obj.search(self.cr, self.uid, [('parent_id', 'child_of', ids)])
            self.acc_sum_list_budget = ids2
        else:
            ids2 = self.acc_sum_list_budget

        query_params = (tuple(ids2), date1, date2, crossovered_budget_id)
        if option == "credit_budget":
            self.cr.execute("SELECT COALESCE(-sum(planned_amount),0.0) \
                    FROM crossovered_budget_lines \
                    WHERE (analytic_account_id IN %s) \
                    AND (date_from<=%s) \
                    AND (date_to>=%s) \
                    AND (planned_amount<0) \
                    AND (crossovered_budget_id=%s)", query_params)
        elif option == "debit_budget":
            self.cr.execute("SELECT COALESCE(sum(planned_amount),0.0) \
                    FROM crossovered_budget_lines \
                    WHERE (analytic_account_id IN %s) \
                    AND (date_from<=%s) \
                    AND (date_to>=%s) \
                    AND (planned_amount>0) \
                    AND (crossovered_budget_id=%s)", query_params)

        return self.cr.fetchone()[0] or 0.0

    def _sum_all(self, accounts, date1, date2, option):
        account_analytic_obj = self.pool.get('account.analytic.account')
        ids = map(lambda x: x['id'], accounts)
        if not ids:
            return 0.0

        if not self.acc_sum_list:
            ids2 = account_analytic_obj.search(self.cr, self.uid, [('parent_id', 'child_of', ids)])
            self.acc_sum_list = ids2
        else:
            ids2 = self.acc_sum_list

        query_params = (tuple(ids2), date1, date2)
        if option == "debit":
            self.cr.execute("SELECT COALESCE(sum(amount),0.0) FROM account_analytic_line \
                    WHERE account_id IN %s AND date>=%s AND date<=%s AND amount>0", query_params)
        elif option == "credit":
            self.cr.execute("SELECT COALESCE(-sum(amount),0.0) FROM account_analytic_line \
                    WHERE account_id IN %s AND date>=%s AND date<=%s AND amount<0", query_params)
        elif option == "quantity":
            self.cr.execute("SELECT COALESCE(sum(unit_amount),0.0) FROM account_analytic_line \
                    WHERE account_id IN %s AND date>=%s AND date<=%s", query_params)

        return self.cr.fetchone()[0] or 0.0

    def _sum_all_plan(self, accounts, date1, date2, option):
        account_analytic_obj = self.pool.get('account.analytic.account')
        ids = map(lambda x: x['id'], accounts)
        if not ids:
            return 0.0

        if not self.acc_sum_list_plan:
            ids2 = account_analytic_obj.search(self.cr, self.uid, [('parent_id', 'child_of', ids)])
            self.acc_sum_list_plan = ids2
        else:
            ids2 = self.acc_sum_list_plan

        query_params = (tuple(ids2), date1, date2)
        if option == "debit_plan":
            self.cr.execute("SELECT COALESCE(sum(amount),0.0) FROM account_analytic_line_plan \
                    WHERE account_id IN %s AND date>=%s AND date<=%s AND amount>0", query_params)
        elif option == "credit_plan":
            self.cr.execute("SELECT COALESCE(-sum(amount),0.0) FROM account_analytic_line_plan \
                    WHERE account_id IN %s AND date>=%s AND date<=%s AND amount<0", query_params)
        elif option == "quantity_plan":
            self.cr.execute("SELECT COALESCE(sum(unit_amount),0.0) FROM account_analytic_line_plan \
                    WHERE account_id IN %s AND date>=%s AND date<=%s", query_params)

        return self.cr.fetchone()[0] or 0.0

    def _sum_all_commit(self, accounts, date1, date2, option):
        account_analytic_obj = self.pool.get('account.analytic.account')
        ids = map(lambda x: x['id'], accounts)
        if not ids:
            return 0.0

        if not self.acc_sum_list_commit:
            ids2 = account_analytic_obj.search(self.cr, self.uid, [('parent_id', 'child_of', ids)])
            self.acc_sum_list_commit = ids2
        else:
            ids2 = self.acc_sum_list_commit

        query_params = (tuple(ids2), date1, date2)
        if option == "debit_commit":
            self.cr.execute("SELECT COALESCE(sum(amount),0.0) FROM account_analytic_line_commit \
                    WHERE account_id IN %s AND date>=%s AND date<=%s AND amount>0", query_params)
        elif option == "credit_commit":
            self.cr.execute("SELECT COALESCE(-sum(amount),0.0) FROM account_analytic_line_commit \
                    WHERE account_id IN %s AND date>=%s AND date<=%s AND amount<0", query_params)
        elif option == "quantity_commit":
            self.cr.execute("SELECT COALESCE(sum(unit_amount),0.0) FROM account_analytic_line_commit \
                    WHERE account_id IN %s AND date>=%s AND date<=%s", query_params)

        return self.cr.fetchone()[0] or 0.0

    def _sum_balance(self, accounts, date1, date2):
        debit = self._sum_all(accounts, date1, date2, 'debit') or 0.0
        credit = self._sum_all(accounts, date1, date2, 'credit') or 0.0
        return (debit - credit)

    def _sum_balance_plan(self, accounts, date1, date2):
        debit = self._sum_all_plan(accounts, date1, date2, 'debit_plan') or 0.0
        credit = self._sum_all_plan(accounts, date1, date2, 'credit_plan') or 0.0
        return (debit - credit)

    def _sum_balance_commit(self, accounts, date1, date2):
        debit = self._sum_all_commit(accounts, date1, date2, 'debit_commit') or 0.0
        credit = self._sum_all_commit(accounts, date1, date2, 'credit_commit') or 0.0
        return (debit - credit)

    def _sum_balance_budget(self, accounts, date1, date2, crossovered_budget_id):
        debit = self._sum_all_budget(accounts, date1, date2, crossovered_budget_id, 'debit_budget') or 0.0
        credit = self._sum_all_budget(accounts, date1, date2, crossovered_budget_id, 'credit_budget') or 0.0
        return (debit - credit)

# report_sxw.report_sxw('report.account.analytic.account.balance.plan', 'account.analytic.account',
#                       'addons/project_cost_analysis/report/analytic_balance_plan.rml',
#                       parser=account_analytic_balance_plan, header="internal")
