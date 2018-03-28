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

#Selects columns with correction values
df = df[['-2', '-1', '+1', '+2']]

#Function to remove all characters after % in the str.  Applies function.
trim_str = lambda x: re.sub("\\%|\\(.*$", "", x)
trim_ws = lambda x:  re.sub(" ", "", x)
df = df.applymap(trim_str)
df = df.applymap(trim_ws)

#Duplicates the rows, because we iterate through N-terminal and lysine
df = df.append(df, ignore_index = True)


#Names of the names attributes to find
TMT10_names = ['TMT10plex-Nter126C',
 'TMT10plex-Nter127N',
 'TMT10plex-Nter127C',
 'TMT10plex-Nter128N',
 'TMT10plex-Nter128C',
 'TMT10plex-Nter129N',
 'TMT10plex-Nter129C',
 'TMT10plex-Nter130N',
 'TMT10plex-Nter130C',
 'TMT10plex-Nter131N',
 'TMT10plex-Lys126C',
 'TMT10plex-Lys127N',
 'TMT10plex-Lys127C',
 'TMT10plex-Lys128N',
 'TMT10plex-Lys128C',
 'TMT10plex-Lys129N',
 'TMT10plex-Lys129C',
 'TMT10plex-Lys130N',
 'TMT10plex-Lys130C',
 'TMT10plex-Lys131N']


#Reads modification.xml
tree = etree.parse('C:/MaxQuant_1.6.0.16/MaxQuant/bin/conf/modifications.xml')
root = tree.getroot()


x = {}
for i,j in enumerate(TMT10_names):
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
