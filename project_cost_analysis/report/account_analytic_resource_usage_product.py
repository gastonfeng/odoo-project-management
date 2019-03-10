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
from odoo import models, fields, tools


class report_account_analytic_resource_usage_product(models.Model):
    _name = "report.account.analytic.resource.usage.product"
    _description = "Resource Usage Analysis by Product"
    _auto = False
    account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True)
    user_id = fields.Many2one('res.users', 'Account Manager')
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_uom_id = fields.Many2one('product.uom', 'UoM', readonly=True)
    amount_real = fields.Float('Real Balance', readonly=True,
                               help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.')
    amount_debit_real = fields.Float('Real Debit', readonly=True,
                                     help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.')
    amount_credit_real = fields.Float('Real Credit', readonly=True,
                                      help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.')
    amount_plan = fields.Float('Planned Balance', readonly=True,
                               help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.')
    amount_debit_plan = fields.Float('Planned Debit', readonly=True,
                                     help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.')
    amount_credit_plan = fields.Float('Planned Credit', readonly=True,
                                      help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.')
    amount_commit = fields.Float('Commited Balance', readonly=True,
                                 help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.')
    amount_debit_commit = fields.Float('Commited Debit', readonly=True,
                                       help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.')
    amount_credit_commit = fields.Float('Commited Credit', readonly=True,
                                        help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.')
    unit_amount_real = fields.Float('Real Quantity', readonly=True, help='Specifies the amount of quantity to count.')
    unit_amount_plan = fields.Float('Planned Quantity', help='Specifies the amount of quantity to count.')
    unit_amount_commit = fields.Float('Commited Quantity', help='Specifies the amount of quantity to count.')
    amount_debit_real_plan = fields.Float('Plan to Real debit deviation', readonly=True)
    amount_debit_real_commit = fields.Float('Commit to Real debit deviation', readonly=True)
    amount_debit_plan_commit = fields.Float('Plan to Commit debit deviation', readonly=True)
    amount_credit_plan_real = fields.Float('Plan to Real credit deviation', readonly=True)
    amount_credit_plan_commit = fields.Float('Plan to Commit credit deviation', readonly=True)
    amount_credit_commit_real = fields.Float('Commit to Real credit deviation', readonly=True)
    amount_real_plan = fields.Float('Real to Planned deviation', readonly=True)

    def init(self):
        """
            @param cr: the current row, from the database cursor,
        """
        tools.drop_view_if_exists(self._cr, 'report_account_analytic_resource_usage_product')

        self._cr.execute("""
            create or replace view report_account_analytic_resource_usage_product as (
                SELECT  
                    ROW_NUMBER() over (order by tot.account_id) as id,
                    sum(tot.unit_amount_real) as unit_amount_real, 
                    sum(tot.unit_amount_plan) as unit_amount_plan, 
                    sum(tot.unit_amount_commit) as unit_amount_commit,
                    sum(tot.amount_real) as amount_real,
                    sum(CASE WHEN tot.amount_real > 0
                         THEN tot.amount_real
                         ELSE 0.0
                         END) as amount_debit_real, 
                    sum(CASE WHEN tot.amount_real < 0
                         THEN -tot.amount_real
                         ELSE 0.0
                         END) as amount_credit_real,       
                    sum(tot.amount_plan) as amount_plan,                        
                    sum(CASE WHEN tot.amount_plan > 0
                         THEN tot.amount_plan
                         ELSE 0.0
                         END) as amount_debit_plan,  
                    sum(CASE WHEN tot.amount_plan < 0
                         THEN -tot.amount_plan
                         ELSE 0.0
                         END) as amount_credit_plan,       
                    sum(tot.amount_commit) as amount_commit,                         
                    sum(CASE WHEN tot.amount_commit > 0
                         THEN tot.amount_commit
                         ELSE 0.0
                         END) as amount_debit_commit,
                    sum(CASE WHEN tot.amount_commit < 0
                         THEN -tot.amount_commit
                         ELSE 0.0
                         END) as amount_credit_commit,      
                    (sum(CASE WHEN tot.amount_plan < 0
                         THEN -tot.amount_plan
                         ELSE 0.0
                         END)-
                         sum(CASE WHEN tot.amount_real < 0
                         THEN -tot.amount_real
                         ELSE 0.0
                         END)
                         ) as amount_credit_plan_real,
                     (sum(CASE WHEN tot.amount_plan < 0
                         THEN -tot.amount_plan
                         ELSE 0.0
                         END)-
                         sum(CASE WHEN tot.amount_commit < 0
                         THEN -tot.amount_commit
                         ELSE 0.0
                         END)
                         ) as amount_credit_plan_commit,     
                     (sum(tot.amount_real)-
                         sum(tot.amount_plan)
                         )as amount_real_plan,                         
                     (sum(CASE WHEN tot.amount_commit < 0
                         THEN -tot.amount_commit
                         ELSE 0.0
                         END)-
                         sum(CASE WHEN tot.amount_real < 0
                         THEN -tot.amount_real
                         ELSE 0.0
                         END)
            )as amount_credit_commit_real,    
                    (sum(CASE WHEN tot.amount_real > 0
                         THEN tot.amount_real
                         ELSE 0.0
                         END)-
                         sum(CASE WHEN tot.amount_plan > 0
                         THEN tot.amount_plan
                         ELSE 0.0
                         END)                         
                         ) as amount_debit_real_plan,   
                    (sum(CASE WHEN tot.amount_real > 0
                         THEN tot.amount_real
                         ELSE 0.0
                         END) -
                         sum(CASE WHEN tot.amount_commit > 0
                         THEN tot.amount_commit
                         ELSE 0.0
                         END)
                         ) as amount_debit_real_commit,
                    (sum(CASE WHEN tot.amount_plan > 0
                         THEN tot.amount_plan
                         ELSE 0.0
                         END) -
                         sum(CASE WHEN tot.amount_commit > 0
                         THEN tot.amount_commit
                         ELSE 0.0
                         END)
                         ) as amount_debit_plan_commit,                    
                    tot.account_id,
                    tot.user_id,
                    tot.product_uom_id,                   
                    tot.product_id
                FROM
                    (SELECT
                         CAST( unit_amount AS FLOAT) AS unit_amount_real, 
                         CAST( 0 AS FLOAT) AS unit_amount_plan, 
                         CAST( 0 AS FLOAT) AS unit_amount_commit,
                         CAST( amount AS FLOAT) AS amount_real, 
                         CAST( 0 AS FLOAT) AS amount_plan,
                         CAST( 0 AS FLOAT) AS amount_commit,                          
                         account_id,
                         user_id, 
                         product_id, 
                         product_uom_id
                    FROM account_analytic_line 
                    WHERE journal_id IN (
                        SELECT id 
                        FROM 
                            account_analytic_journal
                        WHERE
                            type in ('sale','purchase','general'))                    

                UNION ALL
                    SELECT 
                        CAST( 0 AS FLOAT) AS unit_amount_real,
                        CAST( unit_amount AS FLOAT) AS unit_amount_plan,
                        CAST( 0 AS FLOAT) AS unit_amount_commit, 
                        CAST( 0 AS FLOAT) AS amount_real, 
                        CAST( amount AS FLOAT) AS amount_plan, 
                        CAST( 0 AS FLOAT) AS amount_commit,
                        account_id,
                        user_id, 
                        product_id, 
                        product_uom_id
                    FROM account_analytic_line_plan
                    WHERE journal_id in (
                        SELECT id 
                        FROM 
                            account_analytic_journal_plan
                        WHERE
                            type in ('sale','purchase','general'))
                UNION ALL
                    SELECT 
                        CAST( 0 AS FLOAT) AS unit_amount_real,
                        CAST( 0 AS FLOAT) AS unit_amount_plan,
                        CAST( unit_amount AS FLOAT) AS unit_amount_commit, 
                        CAST( 0 AS FLOAT) AS amount_real, 
                        CAST( 0 AS FLOAT) AS amount_plan,
                        CAST( amount AS FLOAT) AS amount_commit, 
                        account_id,
                        user_id, 
                        product_id, 
                        product_uom_id                    
                    FROM account_analytic_line_commit
                    WHERE journal_id in (
                        SELECT id 
                        FROM 
                            account_analytic_journal_commit
                        WHERE
                            type in ('sale','purchase','general'))
                    
                ) AS tot
                GROUP BY 
                    tot.account_id,
                    tot.user_id,
                    tot.product_uom_id,
                    tot.product_id
                    
                ORDER BY tot.account_id

            )""")
