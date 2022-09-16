# -*- coding: utf-8 -*-
"""
IMPC_image_records

Script interacts with the IMPC database to submit a solr query and retreive
results. The query can be modified by adjusting values of the variable 
query_list. The user is prompted by a GUI file dialog for a location to save
the output as a csv

The current query searches for records of images related to the IMPC_XRY_001 
(Xray) procedure performed at BCM.

Created on Fri Sep 16 10:37:18 2022
@author: wardc
"""


#%% import libraries
import pandas
import urllib
import tkinter
import tkinter.filedialog

#%%

# url to the impc image API
url_domain = 'https://www.ebi.ac.uk/mi/impc/solr/impc_images/'

# filter terms for the solr query
query_list = [
    'procedure_stable_id:IMPC_XRY_001',
    'phenotyping_center:BCM'
    ]

# first query is to identify the number of rows to return (set to 0 and check response)
rows_to_return = 0    

url = f'{url_domain}select?q={"%20AND%20".join(query_list)}&rows={rows_to_return}&wt=python'

connection = urllib.request.urlopen(url)
response = eval(connection.read())

print(url)
print('\n')
print(response)


#%% update query url and feed to pandas to extract the data into a df and save

rows_to_return = response['response']['numFound']
url = f'{url_domain}select?q={"%20AND%20".join(query_list)}&rows={rows_to_return}&wt=csv'
# download the data, this may take awhile if large number or records
print('\nDownloading Results\n')
df = pandas.read_csv(url)

print('dataframe created - saving results to csv')

root = tkinter.Tk()
output_text = tkinter.filedialog.asksaveasfilename(
    title='save results',
    defaultextension='.csv'
    )
root.destroy()

if output_text == '' or output_text is None:
    pass
else:
    df.to_csv(output_text)

print('all done')

input('Press ENTER to exit')