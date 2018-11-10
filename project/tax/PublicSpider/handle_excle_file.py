#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/25 16:14
# @Author  : liuyd
# @Site    : 
# @File    : handle_excle_file.py
# @Software: PyCharm
import os
import re
import random
import subprocess
import traceback
import xlrd
import pandas as pd
import os
import platform
from docx import Document
from tax.util import log
from tax.db.basic_db import DbHandle
from tax.db.dbconfig import table_map,match_clos
from tax.city.common.common_db import generate_db_sql
from tax.model.db_config import DBSession
from tax.PublicSpider.get_content_static import HandDb
from tax.model.handle_redis import HandleRedis
from tax.util import log


hr=HandleRedis(7)

session=DBSession()
pl=platform.system()

db=DbHandle()

def read_excel(sheetnum,dbtable,data_source,excelfile,first=True):
    """
    excel 文件不变
    num为表的序号
    :param num:
    :return:
    """
    fheader=False
    try:
        data = xlrd.open_workbook(excelfile)
        table = data.sheets()[sheetnum]
        nrows = table.nrows
        for i in range(nrows):
            fields = table.row_values(i)
            fields=[value.strip() for value in fields if isinstance(value,str)]
            if '纳税人名称' in fields or '法定代表人姓名' in fields or '纳税人名称(姓名)' in fields \
                or '非正常认定日期' in fields or '行政处罚决定书文号' in fields or "单位名称" in fields:
                print(fields)
                fheader = True
                cols = fields
                # read_data_xlrd(table,dbtable,cols,i+1,nrows)
                if first:
                    for kvalue in fields:
                        if kvalue not in table_map[dbtable]:
                            print(kvalue)
                        break
                else:
                    sheetNames = list(data.sheet_names())
                    num_sheet = len(sheetNames)
                    log.crawler.info("num_sheet is:%d" % num_sheet)
                    srow = i
                    # write_cols(cfile,num_sheet,srow)
                    datas = read_data_pandas(dbtable, excelfile, srow, num_sheet, data_source)
                    if datas:
                        return datas
                    break

        if not  fheader:
            print("没有发现头部信息.........")

    except Exception as err:
        print(traceback.format_exc())
        log.error.info("read eror file is:%s"%excelfile)

def read_data_pandas(table,file,srow,num_sheet,data_source,test=False):
    """
    :param table: 数据入库的表名
    :param file: excel文件
    :param srow: 跳过的行数
    :param num_sheet: sheet页数 默认为1
    :return:
    """
    datas=[]
    #统计实际入库的数据量
    intotalnum=0
    db=DbHandle()
    if num_sheet>1:
        log.crawler.info("*"*100)
        log.crawler.info("出现sheet大于1的文件")
    for n_s in range(0,1):
        data = pd.read_excel(file, skiprows=srow,sheet_name=n_s)
        df = pd.DataFrame(data)
        index_li = list(df.columns)
        if index_li:

            colsstr=','.join(index_li)
            log.crawler.info(file+"\n"+colsstr)
            result_dict={}
            for index in index_li:
                if index.strip() in table_map[table]:
                    colname=table_map[table][index.strip()]
                    values=[str(x).strip() for x in list(df[index])]

                    result_dict[colname]=values
            if "身份证件号码" in index_li:
                card_type="身份证"
            else:
                card_type=""
            cols=list(result_dict.keys())
            values_length=len(result_dict[cols[0]])
            if test:
                num=5
            else:
                num=values_length
            for i in range(num):
                try:
                    item={"data_source":data_source}
                    if "card_type" in list(table_map[table].values()):
                        item.update(card_type=card_type)
                    if table=="tb_credit":
                        item.update(credit_level='A')
                    for col in cols:
                        item[col]=result_dict[col][i]
                    datas.append(item)
                    #insert_item_db(table,item)
                except Exception as e:
                    continue

        else:
           continue
    return datas

def insert_item_db(table,item):
    sql=generate_db_sql(table,item)
    r=db.insert_db_func(sql=sql)
    if r:
        log.crawler.info("insert db success table is:%s"%table)


def handle_doc_docx(docfile,table,data_source):
    """
    python 操作word的函数
    :param file:
    :return:
    """
    from win32com import client as wc
    word = wc.Dispatch('Word.Application')
    doc = word.Documents.Open(docfile)

    docxfile=os.path.splitext(docfile)[0]+'.docx'
    doc.SaveAs(docxfile, 12, False, "", True, "", False, False, False, False)
    log.crawler.info("save docx success filename is:%s"%docxfile)
    results=handle_docx(docxfile,table,data_source)
    doc.Close()
    word.Quit()
    return results

def handle_docx(file,dbtable,data_source):
    print("start ...")
    results=[]
    rownum=0
    hd=HandDb(dbtable)
    document = Document(file)  # 读入文件
    tables = document.tables  # 获取文件中的表格集
    if tables:
        log.crawler.info("文档中表格的数量为:%d"%len(tables))
    for i in range(len(tables)):
        clos = []
        table=tables[i]
        rownum=len(table.rows) #获取表格的行数
        log.crawler.info("row num is:%d"%rownum)
        columnum=len(table.columns)
        #循环表格的行数进行内容的读取
        for i in range(rownum):
            """
            找到表格正文开始的位置
            """
            texts=[]
            for j in range(columnum):
                texts.append(table.cell(i,j).text)
            if '纳税人名称' in texts :
                clos=texts
                print(clos)
                snum=i
                clostr=','.join(clos)
                break
        cloitem={}
        if clos:
            for i in range(len(clos)):
                kname=match_clos(dbtable,clos[i])
                if kname:
                    cloitem[i]=kname
            for i in range(snum+1,rownum):
                values=[]
                item = {"data_source":data_source}
                try:
                    for j in range(columnum):
                        value=table.cell(i, j).text
                        values.append(value)
                        if j in cloitem:
                            item[cloitem[j]]=value.strip()
                    if  item.get('tax_type',"中安").isdigit():
                        print("error file",file)
                    results.append(item)
                    # print(item)
                    # sql=hd.generate_sql_dict(item)
                    # if sql:
                    #     db.insert_db_func(sql=sql)
                except Exception as err:
                    print(err)
    return results

def read_excel_by_pandas(file,table,data_source):
    """
    因为对DataFram进行遍历时会跳过第一行也就是标题行
    要是数据有标题没有影响，要是没有标题就会跳过表头,
    因此增加一行作为标题行
    :param file:
    :param table:
    :param data_source:
    :return:
    """
    clitem={}
    print("开始读取excel文档")
    results=[]
    data = pd.read_excel(file,header=0).fillna("")
    headers=list(data.columns)
    clos=[]
    if '序号' in headers or '纳税人名称' in headers or '法定代表人姓名' in headers or '纳税人名称(姓名)' in headers \
            or '非正常认定日期' in headers or '行政处罚决定书文号' in headers or "单位名称" in headers:
        print(headers)
        clos=headers
        for col in headers:
            colname = match_clos(table, col)
            if colname:
                clitem[clos.index(col)] = colname
        for _, row in data.iterrows():
            item={}
            for k,v in clitem.items():
                item[v]=row[k]
            if item:
                item['data_source']=data_source
                results.append(item)

    else:
        print("*"*90)
        for _, row in data.iterrows():
            try:
                item={}
                if not clos:
                    clos = [text.strip() for text in list(row)]
                    print(clos)
                    if '序号' in clos or '纳税人名称' in clos or '法定代表人姓名' in clos or '纳税人识别号' in clos \
                            or '非正常认定日期' in clos or '行政处罚决定书文号' in clos or "单位名称" in clos:
                        continue
                if clos and not clitem:
                    for col in clos:
                        colname=match_clos(table,col)
                        if colname:
                            clitem[clos.index(col)]=colname
                for k,v in clitem.items():
                    item[v]=list(row)[k]
                if table=="tb_qsgg" and item['company']!='':
                    item['data_source']=data_source
                    results.append(item)
                elif table=="tb_credit" and item['name']!='':
                    item['data_source'] = data_source
                    results.append(item)
                else:
                    item['data_source']=data_source
                    results.append(item)
            except:
                continue
    log.crawler.info("读取excel文档数据的长度为:%d"%len(results))
    return results

def read_doc_linux(table,file):
    results=[]
    clos = []
    outtext = subprocess.check_output(["antiword",file]).decode()
    lines = outtext.split("\n")
    for line in lines:
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        texts = line.split("|")
        contents = [text.strip() for text in texts]
        print(contents)
        if not clos:
            if '纳税人名称' in contents or '法定代表人姓名' in contents or '纳税人名称(姓名)' in contents \
                    or '非正常认定日期' in contents or '行政处罚决定书文号' in contents or "单位名称" in contents:
                clos = contents
                continue
        if clos:
            if len(contents)==len(clos):
                item={}
                for clo in clos:
                    field_dict=table_map[table]
                    if clo in field_dict:
                        item[field_dict[clo]]=contents[clos.index(clo)]
                results.append(item)
            else:
                continue
    return results


if __name__=='__main__':
    table="tb_xzcf"
    data_source="XiZang"
    file="D:\\data\\tax\\tb_xzcf\\5a2cd6771f144208bdb334518af60ca3.xls"
    r=read_excel_by_pandas(file,table,data_source)
    print(r)
