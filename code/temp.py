import os
import re
import inflect
import  pandas as pd
basepath = '/home/nani/hcl/HCL ML Challenge/HCL ML Challenge Dataset1/'
tail=['statements']
p = inflect.engine()
words = p.number_to_words(1234)
print(words)

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def rreplace(s, old, new):
    return (s[::-1].replace(old[::-1],new[::-1], 1))[::-1]

#Resultant Dataframe
resultant_df=pd.DataFrame(columns=['Filename', 'Extraced_values'])

for entry in os.listdir(basepath):
        print(entry)
	input_file = open(basepath+entry)
	content=input_file.read()
	content=content.lower()
	content=content.replace('\r\n','\n')
	content=re.sub(' +',' ',content)
	content=re.sub('notes','',content)
	# Remove the header
	content=re.sub('.*[0-9]+ +\n','',content,1)
	# Remove the tail
	for delimiter in tail:
		content=re.sub(delimiter+'[^`]+','',content,re.DOTALL)
	#Remove the symbol Row
	content=re.sub('[\xc2].*\n ','',content,re.MULTILINE)
	content=re.sub('[(),]','',content)
	#count of no of years present
	count=len(content.split('\n')[0].strip().split(' '))
	#Removing unnecessary new lines b/w text
	required_content=""
	for line in content.split('\n'):
		line=line.rstrip()
		if hasNumbers(line):
			required_content+=line+'\n'
		else:
			required_content+=line
	required_content=re.sub(' +',' ',required_content).rstrip()
	#print(required_content)
	text=""
	for line in required_content.split('\n'):
		for i in range(count):
			line=rreplace(line," ",";")
		text+=line+'\n'
	text=text.strip()
	print(text)
	df = pd.DataFrame([x.split(';') for x in text.split('\n')])
	df.columns = df.iloc[0]
	df = df.reindex(df.index.drop(0)).reset_index(drop=True)
	df.columns.name = None				
	df.rename(columns={'':'notes'}, inplace=True)	
	df=df.filter(items=['notes','2019'])
	df=df.set_index('notes')
	required_df=df.T
	required_df=required_df.to_json(orient='records')
	if '2019' in df:
		resultant_df=resultant_df.append({'Filename':entry,'Extraced_values':required_df}, ignore_index=True)	
	else:
		resultant_df=resultant_df.append({'Filename':entry,'Extraced_values':'NA'}, ignore_index=True)
print(resultant_df)
resultant_df.to_csv(basepath+'out.csv', index=False)
