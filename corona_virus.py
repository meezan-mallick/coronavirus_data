#!/usr/bin/env python
# coding: utf-8

# # Python script to get corona virus data by Meezan Malek

from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

source = requests.get('https://www.mohfw.gov.in/').text  #source of the covid-19 website
soup = BeautifulSoup(source,'lxml')  #html parser 

row_list = list()    #will contain list of rows [tr1.tr2.tr3]
data=list()         #main data frame list  [ [1,abc],[2,bcd] ]

table = soup.find('table',class_="table table-striped")

rows = table.find_all('tr') #it will return the list of tr's from the table
for r in rows:
    list_of_td = [td.get_text() for td in r.find_all('td')] #it will return the list of td's from a particular tr
    row_list.append(list_of_td)


for i in row_list:
    data.append(i)

df = pd.DataFrame(data, columns=['N0', 'state', 'Total Confirmed cases', 'Cured/Discharged', 'Death'])
#df.to_excel('corona_virus.xlsx', sheet_name='sheet1', index=False)

df = df.drop([0,33,34,35])

sorted_df=df.sort_values(by='Total Confirmed cases',ascending=False)

print(sorted_df[['state','Total Confirmed cases']])

