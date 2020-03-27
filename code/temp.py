# coding: utf8
import os
import re
import sys
import  pandas as pd
basepath = '/home/nani/hcl/HCL ML Challenge/HCL ML Challenge Dataset/'
tail=['statements','®','notes to the','===','for the year ending','the company']

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def rreplace(s, old, new):
    return (s[::-1].replace(old[::-1],new[::-1], 1))[::-1]

#Resultant Dataframe
resultant_df=pd.DataFrame(columns=['Filename', 'Extraced_values'])

for entry in os.listdir(basepath):
	try:
		#print(entry)
		input_file = open(basepath+entry)
		content=input_file.read()
		content=content.lower()
		content=content.replace('\r\n','\n')
		content=re.sub('[,£{}]','',content)
		content=re.sub('\((\d+)\)',r'-\1',content)
		content=re.sub(' +',' ',content)
		content=re.sub('registered number.*\n','',content)
		#Removing unnecessary new lines b/w text
		required_content=""
		for line in content.split('\n'):
			line=line.rstrip()
			if hasNumbers(line):
				required_content+=line+'\n'
			else:
				required_content+=line
		required_content=re.sub(' +',' ',required_content).rstrip()
		# Remove the header
		required_content=re.sub('.*[0-9]+\n','',required_content,1)
		# Remove the tail
		for delimiter in tail:
			required_content=re.sub(delimiter+'[^`]+','',required_content,re.DOTALL).rstrip()
		required_content=required_content.replace('notes','')
		required_content=re.sub(r"([0-9]+)/([0-9]+)/([0-9]+)",r"\3",required_content)
		#print(required_content)
		#count of no of years present
		count=len(list(x for x in required_content.split('\n')[0].strip().split(' ') if int(x) <= sys.maxint))
		#print(required_content.split('\n')[0].strip().split(' '))
		text=""
		for line in required_content.split('\n'):
			for i in range(count):
				line=rreplace(line," ",";")
			text+=line+'\n'
		text=text.strip()
		#print(text)
		df = pd.DataFrame([x.split(';') for x in text.split('\n')])
		df.columns = df.iloc[0]
		df = df.reindex(df.index.drop(0)).reset_index(drop=True)
		df.columns.name = None	
		#print(df)			
		df.rename(columns={'':'notes'}, inplace=True)	
		df=df.filter(items=['notes','2019'])
		df=df[(df['notes'] != '')]
		df['2019'][(df['2019']=='-')]='nan'
		#print(df)
		df=df.set_index('notes')
		required_df=df.T
		required_df=required_df.to_json(orient='records')
		if '2019' in df:
			resultant_df=resultant_df.append({'Filename':entry,'Extraced_values':required_df}, ignore_index=True)	
		else:
			resultant_df=resultant_df.append({'Filename':entry,'Extraced_values':'NA'}, ignore_index=True)
	except:
		print (entry)		
		continue
print(resultant_df)
resultant_df.to_csv('/home/nani/hcl/HCL ML Challenge/Results.csv', index=False)
