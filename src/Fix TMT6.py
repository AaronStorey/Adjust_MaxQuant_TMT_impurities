print("\n \n \nThis current script will fix the TMT-10plex impurity values for MaxQuant 1.6.0.16")
print("\nStarting script, this should take around 10 seconds... \n")

import pandas as pd
from lxml import etree
import re
import sys
import os
import tabula


#Finds files matching ".pdf" file in the ./input folder.
pdf_file = input("Please drag the lot number.pdf file into the console,\nthen click on the console, then press Enter: \n")

pdf_file = re.sub("\\\\", '/', pdf_file)
pdf_file = re.sub('\"', '', pdf_file)

#Reads table from pdf and saves as csv in output
df = tabula.read_pdf(pdf_file, output_format="csv")

#Cleans table
if len(df.transpose()) == 6:
    df = df[['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2','Unnamed: 4', 'Unnamed: 5']]
    df = df.rename(index = str, columns ={'Unnamed: 0':'TMT', 'Unnamed: 1':'-2', 'Unnamed: 2':'-1', 'Unnamed: 4':'+1', 'Unnamed: 5':'+2'})
    df = df.dropna()
    df = df[1:]

#Cleans table
if len(df.transpose()) == 8:
    df = df[['Unnamed: 0', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 6', 'Unnamed: 7']]
    df = df.rename(index = str, columns ={'Unnamed: 0':'TMT', 'Unnamed: 3':'-2', 'Unnamed: 4':'-1', 'Unnamed: 6':'+1', 'Unnamed: 7':'+2'})
    df = df.dropna()
    df = df[1:]


#Function to remove all characters after % in the str.  Applies function.
trim_str = lambda x: re.sub("\\%|\\(.*$", "", x)
trim_ws = lambda x:  re.sub(" ", "", x)
df = df.applymap(trim_str)
df = df.applymap(trim_ws)

#Duplicates the rows, because we iterate through N-terminal and lysine
df = df.append(df, ignore_index = True)


#Names of the names attributes to find
TMT6_names = ['TMT6plex-Nter126',
'TMT6plex-Nter127',
'TMT6plex-Nter128',
'TMT6plex-Nter129',
'TMT6plex-Nter130',
'TMT6plex-Nter131',
'TMT6plex-Lys126',
'TMT6plex-Lys127',
'TMT6plex-Lys128',
'TMT6plex-Lys129',
'TMT6plex-Lys130',
'TMT6plex-Lys131']

#Reads modification.xml
tree = etree.parse('C:/MaxQuant_1.6.0.16/MaxQuant/bin/conf/modifications.xml')
root = tree.getroot()


x = {}
for i,j in enumerate(TMT6_names):
    x['Name'] = j
    x['reporterCorrectionM2'] = df['-2'][i]
    x['reporterCorrectionM1'] = df['-1'][i]
    x['reporterCorrectionP1'] = df['+1'][i]
    x['reporterCorrectionP2'] = df['+2'][i]
    for k in root.iter("modification"):
        if re.match(x['Name'], k.get('title')):
            k.set('reporterCorrectionM2', x['reporterCorrectionM2'])
            k.set('reporterCorrectionM1', x['reporterCorrectionM1'])
            k.set('reporterCorrectionP1', x['reporterCorrectionP1'])
            k.set('reporterCorrectionP2', x['reporterCorrectionP2'])

tree.write('C:/MaxQuant_1.6.0.16/MaxQuant/bin/conf/modifications.xml', xml_declaration=True, encoding ="utf-8", method = "xml")
print("\n \n \n \nThe new file was created.  Open a fresh MaxQuant 1.6.0.16 session and check that the values are correct. \n \n \n")
