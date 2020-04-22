#!/usr/bin/env python
# coding: utf-8

# # Python script to get corona virus data by Meezan Malek

# In[29]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt


# In[44]:


source = requests.get('https://www.mohfw.gov.in/').text
soup = BeautifulSoup(source,'lxml')


mylist = list()

table = soup.find('table',class_="table table-striped")

with open('Corona_virus.txt','w') as r:
    r.write("N0".ljust(30))
    r.write("State".ljust(30))
    r.write("Total Confirmed cases".ljust(30))
    r.write("Cured/Discharged".ljust(30))
    r.write("Death".ljust(30))
    
    
    for row in table.find_all('tr'):
        for cell in row.find_all('td'):
            r.write(cell.text.ljust(30))
        r.write('\n')
        
print("data saved in text file : corona_virus.txt")


# In[36]:


source = requests.get('https://www.mohfw.gov.in/').text  #source of the covid-19 website
soup = BeautifulSoup(source,'lxml')  #html parser 

row_list = list()    #will contain list of rows [tr1.tr2.tr3]
data=list()         #main data frame list  [ [1,abc],[2,bcd] ]

table = soup.find('table',class_="table table-striped")

rows = table.find_all('tr') #it will return the list of tr's from the table
for r in rows:
    list_of_td=r.find_all('td') #it will return the list of td's from a particular tr
    row_list.append(list_of_td)


for i in row_list:
    data.append(i)

df = pd.DataFrame(data,columns=['N0','state','Total Confirmed cases','Cured/Discharged','Death'])
df.to_excel('corona_virus.xlsx', sheet_name='sheet1', index=False)
df
print("data stored in excel file : corona_virus.xlxs")

