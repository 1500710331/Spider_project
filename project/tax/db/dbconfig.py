#!/usr/bin/env python
# encoding: utf-8
'''
@author: liuyd
@file: dbconfig.py
@time: 2018/8/14 16:29
@desc:
'''

table_map={



"tb_enterprise_list":{
'公司地址':'ADDRESS',
"固定电话":'phone',
'邮政编码':'EMAIL',
'法人名称':'ENTERPRISE_NAME',
'营业执照号码':'BUSI_NO'

},
"tb_qsgg":{
    '企业或单位名称':'company',
    '业户名称':'company',
    '名称':'company',
'纳税人名称(姓名)':'company',
'纳税人名称':'company',
'企业名称':"company",
'社会信用代码（纳税人识别号）':'identity_num',
'纳税人识别号':"identity_num",
'法定代表人':'name',
    '法人姓名':'name',
 '业主姓名':'name',
'法人代表姓名':"name",
'法定代表人或负责人姓名':'name',
'法定代表人或负责人姓名（业主姓名）':'name',
'法定代表人（负责人）':'name',
'企业法定代表人或负责人姓名（个体业主姓名）':'name',
'法定代表人（负责人）姓名':'name',
'证件种类':"card_type",
'身份证件号码':'card_id',
'居民身份证或其他有效身份证明':'card_id',
'居民身份证或其他有效身份证件号码（身份证件出生月日4位以*替代）':'card_id',
'居民身份证或其他有效身份证件号码':'card_id',
'居民身份证号或其他有效身份证件号码':'card_id',
'居民身份证号码':'card_id',
'证件号码':"card_id",
'经营地点':"address",
'生产经营地址':'address',
'主管税务所（科、分局）':'publish_org',
'欠税税种':'tax_type',
'税种':"tax_type",
'欠税余额(元)':'tax_amount',
'欠税余额（元）':"tax_amount",
'欠税余额（单位：元）':'tax_amount',
'欠税金额(元)':"tax_amount",
'欠税金额':'tax_amount',
'欠税余额':'tax_amount',
'其中：当期新发生欠税金额':'new_tax_amount',
'当期新发生的欠税金额(元)':'new_tax_amount',
'当期所发生的欠税余额(元)':"new_tax_amount",
'当期新发生的欠税金额':"new_tax_amount"
},

"tb_credit":{
'统一社会信用代码.纳税人识别号':'reco_code',
'信用代码或识别号':'reco_code',
'统一社会信用码（纳税人识别号）':'reco_code',
'税务登记号':'reco_code',
'纳税人识别号':'reco_code',
'纳税人名称':'name',
'信用等级':'credit_level',
'年度':'which_year',
'主管税务机关':'which_state',
'纳税人主管税务机关':'which_state',
'主管国税机关':'which_state',
'税务管理机关':'which_state',
'税务机关名称':'which_state',
'评价年度':'which_year',
'所属年度':'which_year',
'评定年度':'which_year',
'税务机关':'which_year'
},

"tb_hundred":{
'纳税人识别号':'reco_code',
'纳税人名称':'reco_name',
'入库税款':'tax_money'

},
"tb_fzch":{
    "纳税人识别号":"identity_num",
    "纳税人名称":"company",
    "税务登记号":"tax_reg_num",
    "公司名称":"company",
    "纳税人状态":"status",
    "认定原因":"reason",
    "非正常认定日期":"considered_date",
    "认定日期":"considered_date",
    '非正常户认定日期':'considered_date',
    "认定税务机关":"tax_authority",
    "认定机关":"tax_authority",
    "主管税务机关名称":"tax_authority",
    '主管税务所（科、分局）':'tax_authority',
    "税务机关":"tax_authority",
    "法人代表或负责人":"name",
    '法定代表人（负责人、业主）姓名':"name",
    "业主姓名":"name",
    "法人证件类型代码":"card_type",
    '身份证件种类':'card_type',
    "公开类型":"kind",
    "注册地址":"address",
    "生产经营地址":"address",
    "法定代表人身份证号码":"id_card",
    "身份证件号码":"id_card",
    "法人证件号码":"id_card",
    "登记注册类型":"reg_type"
},
'tb_xzcf':{
'行政处罚决定书文号':'case_no',
    '文,号':'case_no',
    '文号':'case_no',
    '文书字轨':'case_no',
    '字轨':'case_no',
'处罚名称':'case_name',
    '名称':'case_name',
'案件名称':'case_name',
'违法行为名称':'case_name',
'处罚类别':'case_cate',
'处罚事由':'case_reason',
'税收违法手段':'case_reason',
'税收违法类型':'case_tax_type',
'处罚依据':'case_base',
'行政相对人名称':'name',
'纳税人名称':'name',
"纳税识别号": "identity_num",

'行政相对人统一社会信用代码':'org_code',
'社会信用代码（纳税人识别号）':'org_code',
'统一社会信用代码':'org_code',
'行政相对人代码-1（统一社会信用代码）':'org_code',
'行政相对人代码_1 (统一社会信用代码)':'unique_code',
'行政相对人代码_2 (组织机构代码)':'org_code',
'行政相对人代码（统一社会信用代码或纳税人识别号）':'org_code',


'行政相对人代码_3 (工商登记码)':'gs_code',
'行政相对人代码_4 (税务登记号)':'tax_code',
'居民身份证号码':'admin_cardno',
'行政相对人代码-5（居民身份证号）':'admin_cardno',
'法定代表人身份证号码':'admin_cardno',
'法定代表人或者负责人证件号码':'admin_cardno',
'法定代表人身份证':'admin_cardno',
'法定代表人或者负责人姓名':'legal_name',
'法定代表人姓名':'legal_name',
'处罚结果':'cf_result',
'应缴罚款金额':'cf_result',
'处罚结果（应缴罚款金额）':'cf_result',
'处罚决定日期':'punish_date',
'文书制作日期':'punish_date',
'处罚生效期':'punish_effected_date',
'处罚生效期起':'punish_effected_date',
'处罚截止日期':'punish_closing_date',
'处罚生效期止':'punish_closing_date',
'处罚截止期':'punish_closing_date',
'公示期限':'public_limit',
'处罚机关':'cf_gov',
    '作出处罚决定的部门':'cf_gov',
'主管税务机关':'cf_gov',
'当前状态':'current_status',
'地方编码':'local_code',
'数据更新时间戳':'data_update_date',
'数据更新时间':'data_update_date'
},
    'tb_wfaj':{
'纳税人名称':'name',
'纳税人识别号':'reco_code',
'组织机构代码':'org_code',
'注册地址':'address',
'法定代表人或者负责人姓名、性别、证件名称及号码':'legal_man',
'法定代表人姓名、性别及身份证号码':'legal_man',
'负有直接责任的财务负责人姓名、性别、证件名称及号码':'finace_man',
'财务负责人姓名、性别及身份证号码':'finace_man',
'负有直接责任的中介机构信息及其从业人员信息':'agency_man',
'负有直接责任的中介机构信息':'agency_man',
'案件性质':'case_property',
'违法事实':'case_base',
'主要违法事实':'case_base',
        '处罚情况':'cf_result',
'相关法律依据及,税务处理处罚情况':'cf_result',
'相关法律依据及税务处理处罚情况':'cf_result'

},
"TB_SHIXIN_PERSON":{
    "执行案号":"CASE_CODE",
    "案号":"CASE_CODE",
    "企业法人/负责人姓名":"PNAME",
    "失信被执行人姓名／名称":"PNAME",
    "姓名":"PNAME",
    '性别':"SEX_NAME",
    '年龄':'AGE',
    '身份证号':'CARD_NUM',
    '身份证号码／组织机构代码':'CARD_NUM',
    '地域名称':'PLACE',
    '执行法院':'COURT_NAME',
    '执行依据文号':'EXEC_CODE',
    '作出执行依据单位':'GIST_UNIT',
    '法律生效文书确定的义务':'DUTY',
    "被执行人的履行情况":"EXEC_SITUATION",
    "失信被执行人具体情形":"FACTS",
    "立案时间":"CREATE_TIME",
    "发布时间":"PUBLISH_TIME",
    "已履行部分":"PERFORM",
    "未履行部分":"NOT_PERFORM"
},
"TB_LIMIT_HIGHCONS":{
    "案号":"CASE_CODE",
    "企业法人/负责人姓名":"PNAME",
    '失信被执行人姓名／名称':'PNAME',
    "姓名":"PNAME",
    '性别':"SEX_NAME",
    '年龄':'AGE',
    '身份证号':'CARD_NUM',
    '身份证号码／组织机构代码':'CARD_NUM',
    '地域名称':'PLACE',
    '执行法院':'COURT_NAME',
    '执行依据文号':'EXEC_CODE',
    '作出执行依据单位':'GIST_UNIT',
    '法律生效文书确定的义务':'DUTY',
    "被执行人的履行情况":"EXEC_SITUATION",
    "失信被执行人具体情形":"FACTS",
    "立案时间":"CREATE_TIME",
    "发布时间":"PUBLISH_TIME",
    "已履行部分":"PERFORM",
    "未履行部分":"NOT_PERFORM"

}
}


def match_clos(table,col):
    if table=="tb_qsgg":
        if "名称" in col:
            name="company"
        elif '纳税人识别号' in col or '社会信用代码' in col :
            name="identity_num"
        elif  "姓名" in col:
            name="name"
        elif "身份证" in col or '证件号码' in col:
            name="card_id"
        elif "证件类型" in col:
            name="card_type"
        elif '地址' in col or "地点" in col:
            name="address"
        elif '税种' in col:
            name="tax_type"
        elif '欠税余额' in col:
            name="tax_amount"
        elif "新" in col or '当期' in col:
            name="new_tax_amount"
        else:
            name=None
        return name
    elif table=="tb_credit":
        if "年度" in col:
            name='which_year'
        elif '信用代码 ' in col or "纳税人识别号" in col:
            name="reco_code"
        elif '名称' in col:
            name="name"
        elif "机关" in col:
            name="which_state"
        else:
            name=None
        return name

    elif table=="tb_xzcf":
        if '文号' in col:
            name="case_no"
        elif '事由' in col:
            name='case_reason'
        elif '行政相对人名称' in col:
            name='name'
        elif '机关' in col:
            name='cf_gov'
        elif "信用代码" in col:
            name="org_code"
        elif '案件名称' in col:
            name='case_name'
        elif '处罚类别' in col:
            name='case_cate'
        elif '依据' in col:
            name='case_base'
        elif '身份证' in col:
            name='admin_cardno'
        elif '姓名' in col:
            name='legal_name'
        elif '结果' in col:
            name='cf_result'
        elif '处罚生效期' in col:
            name='punish_effected_date'
        elif '截止' in col:
            name='punish_closing_date'
        elif '公示期限' in col:
            name='public_limit'
        elif '当前状态' in col:
            name="current_status"
        elif '时间戳' in col:
            name='data_update_date'
        else:
            name=None

    return name




if __name__=='__main__':
   datas=['社会信用代码', '纳税人名称', '法人姓名', '身份证件号码', '生产经营地址', '征收项目', '欠税余额', '当期发生欠税']
   for data in datas:
       a=match_clos('tb_qsgg',data)
       print(a)






