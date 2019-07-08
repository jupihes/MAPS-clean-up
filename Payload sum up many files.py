
# -*- coding: utf-8 -*-
"""
Aggregate cell or site level payload terms, read files of MAPS excel dump and remove first row generated by MAPS
group by in site level

change column format to avoid type issue
@author: hesam.mo
Created on Sat Mar 16 17:43:59 2019
"""
import pandas as pd
from pandas import ExcelWriter
import numpy as np
import os as oss

address = r'D:\Payload sum up'
oss.chdir(address) ## change working directory to folder we need
l = oss.listdir(address)

dff = pd.DataFrame()
d = {'2G.xls':'2G BTS','3G.xls':'3G NODEB', '4G_FDD.xls':'4G LTE ENODB'}

for file_name in ['2G.xls','3G.xls', '4G_FDD.xls']:
	
	df = pd.read_excel(file_name,skiprows = 1)#, sheet_name='2G') ## read excel with name = file_name 
	df.columns = df.columns.str.upper() ## chnage all column namse to upper 
	df['BTS'] = df[d.get(file_name)].str.extract('([A-Z][\d]{4})')  ## regex to find site ID pattern and write it in new column
	df.loc[df['BTS'].isna() ==True, 'BTS'] = 'Not correct SiteID'
	pay_cols = [col for col in df.columns if 'PAYLOAD' in col]
	#print(list(df.columns))
	print(pay_cols)
	print(df.shape)
	df = df.rename(columns={pay_cols[0]:'PAYLOAD(MB)'})
	#df['PAYLOAD(MB)'] = df['PAYLOAD(MB)']/1000
	dff_temp = df[['TIME','BTS', 'PAYLOAD(MB)']]
	dff = dff.append(dff_temp)
	#df.to_excel(writer,'3G')
	del df, dff_temp

writer = ExcelWriter(r'D:\all-revised-new.xlsx')
dff.to_excel(writer,'all')
dfff = dff.pivot_table(dff,index=['BTS'], columns=['TIME'],aggfunc=np.sum)
dfff.to_excel(writer,'summary')
print(dfff.shape)
print('Payload Sums are:\n',dff.groupby('TIME').agg(sum))
print(dff.TIME.dt.days_in_month.unique())
for i in range(0,len(dff.TIME.dt.days_in_month.unique())):
	print('Avg Payload/day for ',dff.TIME.dt.month_name().unique()[i],' is ', dff.groupby('TIME').agg(sum).iloc[i,0]/dff.TIME.dt.days_in_month.unique()[i])

writer.save()
