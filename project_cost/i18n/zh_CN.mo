��    j      l  �   �      	  #   	  !   5	     W	     h	     t	     {	     �	     �	     �	     �	     �	     �	     �	     �	     	
     &
     7
     F
  !   W
     y
     �
     �
     �
     �
     �
            �   .     �     �     �     �     �     �          .     H     e     x     �     �     �     �     �     �     �  0  �       	           N   (  6   w     �     �     �     �  �   �     �  h   �       	     	        )     /     6  	   B     L     d     t     �     �     �     �     �     �     
     %     ;     Q  "   W      z     �     �     �     �     �     �     �     �     �  	   
  *        ?  S   O  U   �  =   �  B   7  A   z  �   �  �   Y     �     �                 n       �     �     �  	   �     �     �  	   �     �     �                    '     4     A     T     a     n     {     �     �     �     �     �     �             j   &     �     �     �     �     �     �     �     �     �               2     E     L     S     Z     a     h  �  o     �              4      .   J      y      �      �      �   �   �   	   7!  S   A!     �!     �!     �!     �!     �!     �!  	   �!     �!     �!     �!     "     "     %"     8"     K"     ^"     q"     �"     �"     �"     �"     �"     �"     �"     �"     #     #     #     #     !#     4#     A#     H#     d#  H   q#  H   �#  9   $  4   =$  0   r$  �   �$  �   ,%     �%     �%     �%     �%     �%     D   C              M              \          .           -              c   U       %   !   N   (   I          [   3                    A   R      ?      ;       f   S       5         "   `   a          )   H   F   2   *   +   W   G   8       4                 d   i   O   '          @             9   _               ]       ^      &   #             >   ,   B   e       T   /   Y       b   6          0       Q      :   h                      j      
   =   7   J          V                         1   E       g   	   Z   $   K   L       P   X           <        Account Analytic Commitment Journal Account Analytic Planning Journal Account currency Account n° Active Actual Analytic journal Administration Amount Amount Currency Amount currency Analytic Analytic Account Analytic Accounting Analytic Accounts Analytic Commitments Journal Analytic Entries Analytic Entry Analytic Journal Analytic Journal Commitment Items Analytic Journal Commitments Analytic Journal Plan Analytic Journal Plan Items Analytic Journals Analytic Line Analytic Line Commitment Analytic Line Plan Analytic Planning Journal Calculated by multiplying the quantity and the price given in the Product's cost price. Always expressed in the company main currency. Cancel Cash Code Commitment Analytic Entries Commitment Analytic Journal Commitment Analytic Journals Commitment Balance Commitment analytic lines Commitments Analytic Journal Commitments Credit Commitments Journal Code Commitments Journal Name Company Costs Currency Date Description Edit Eficent Project Management. Project Cost Planning
        - A planning analytic journal object is created. It is similar to the analytic journal, but used for planning purposes
        - The planning analytic journals can be configured
        - A planning analytic journal lines object is created, with the exceptions of referencing 
        to the planning analytic journal instead of the analytic journal, and considering 
        that the general account is not a required entry.
        - The new object is visible as a separate entity, accesible from the Accounting area, with the corresponding search, tree, form views.
        - New analytic account attributes: cumulated planned costs, cummulated planned earnings and cumulated balance.
        The attributes are calculated based on the planning analytic journal lines. 
        The new attributes are visible on the following views:
            − Analytic account forms: cumulated planned costs, cumulated planned earnings and cumulated balance
            − Budget positions: cumulated planned costs
 
     End of period Entries:  Error ! Error! The currency has to be the same as the currency of the selected company Error! You can not create recursive analytic accounts. Extended Filters... General General Account General Accounting Gives the type of the analytic journal. When it needs for a document (eg: an invoice) to create analytic entries, OpenERP will look for a matching journal of the same type. Group By... If the active field is set to False, it will allow you to hide the analytic journal without removing it. Lines Move Line Move Name Notes Period Period from Period to Plan Costs and Revenues Planned Balance Planned Commitments Planned Credit Planned Debit Planned analytic lines Planning Analitic Journal Planning Analytic Entries Planning Analytic Journal Planning Analytic Journals Planning Journal Code Planning Journal Name Print Print Commitment Analytic Journals Print Planning Analytic Journals Product Product Information Project Management Purchase Quantity Ref. Sale Search Analytic Lines Select Period Situation Specifies the amount of quantity to count. Start of period The amount expressed in an optional other currency if it is a multi-currency entry. The amount expressed in the related account currency if not equal to the company one. The related account currency if not equal to the company one. There is no expense account defined for this product: "%s" (id:%d) There is no income account defined for this product: "%s" (id:%d) To print a commitments analytics (or costs) journal for a given period. The report give code, move name, account number, general amount and analytic amount. To print a planning analytics (or costs) journal for a given period. The report give code, move name, account number, general amount and analytic amount. Total Total Quantity Type UoM User Project-Id-Version: OpenERP Server 6.0.3
Report-Msgid-Bugs-To: support@openerp.com
POT-Creation-Date: 2012-12-27 08:36+0000
PO-Revision-Date: 2019-03-10 22:23+0800
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=1; plural=0;
X-Generator: Poedit 2.2.1
Last-Translator: 
Language: zh_CN
 账户分析承诺日志 账户分析计划日志 账户币种 帐号n° 有效 实际分析日志 管理员 数量 金额货币 金额货币 分析 分析账户 分析会计 分析账户 分析承诺日志 分析条目 分析条目 分析日志 分析日志承诺项目 分析日志承诺 分析日志计划 分析日志计划项目 分析日志 分析明细 分析明细承诺 分析明细计划 分析计划日志 通过乘以产品成本价格中给出的数量和价格来计算。 始终以公司主要货币表示。 取消 现金 代码 承诺分析条目 承诺分析日志 承诺分析日志 承诺余额 承诺分析明细 承诺分析日志 承诺信用 承诺日志代码 承诺日志名称 公司 成本 货币 日期 说明 编辑 有效的项目管理。项目成本计划
         - 创建计划分析日记对象。它类似于分析期刊，但用于规划目的
         - 可以配置计划分析日记帐
         - 创建计划分析日记帐行对象，但引用除外
        到计划分析期刊而不是分析期刊，并考虑
        普通帐户不是必填项。
         - 新对象作为单独的实体可见，可从会计区域访问，具有相应的搜索，树，表单视图。
         - 新的分析帐户属性：累计计划成本，累计计划收入和累计余额。
        属性基于计划分析日记帐行计算。
        新属性在以下视图中可见：
             - 分析账户表格：累计计划成本，累计计划收益和累计余额
             - 预算职位：累计计划成本
    期间结束 项:  错误! 错误！ 货币必须与所选公司的货币相同 错误！ 您无法创建递归分析帐户。 附加筛选... 常规 通用账户 基础会计 提供分析日志的类型。 当需要文档（例如：发票）来创建分析条目时，OpenERP将查找相同类型的匹配日志。 分组... 如果活动字段设置为False，则允许您隐藏分析日志而不删除它。 明细 移动明细 移动名称 备注 期间 期间起始 期间到 计划成本和收入 计划余额 计划承诺 计划信贷 计划借记 计划分析明细 计划分析日志 计划分析条目 计划分析日志 规划分析日志 计划日志代码 计划日志名称 打印 打印承诺分析日志 打印计划分析日志 产品 产品信息 项目管理 采购 数量 引用. 销售 搜索分析明细 选择期间 情境 指定要计算的数量。 开始时期 如果是多货币条目，则以可选的其他货币表示的金额。 如果不等于公司货币，则以相关账户货币表示的金额。 相关的账户货币，如果不等于公司的货币。 没有为此产品定义费用帐户： "%s" (id:%d) 此产品没有定义收入帐户："%s" (id:%d) 打印特定时期的承诺分析（或成本）日记帐。 报告提供代码，移动名称，帐号，一般金额和分析金额。 打印特定时期的计划分析（或成本）日记帐。 报告提供代码，移动名称，帐号，一般金额和分析金额。 总计 数量总计 类型 产品单位数量 用户 