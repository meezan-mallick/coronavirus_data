#Python script to get corona virus data by Meezan Malek

from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

source = requests.get('https://www.mohfw.gov.in/').text  # source of the covid-19 website
soup = BeautifulSoup(source, 'lxml')  # html parser

mylist = list()
table = soup.find('table', class_="table table-striped")

with open('Corona_virus.txt', 'w') as r:
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

#____________________saving data into excel______________________________________

row_list = list()  # will contain list of rows [tr1.tr2.tr3]
data = list()  # main data frame list  [ [1,abc],[2,bcd] ]

table = soup.find('table', class_="table table-striped")

rows = table.find_all('tr')  # it will return the list of tr's from the table
for r in rows:
    list_of_td = [td.get_text() for td in r.find_all('td')]  # it will return the list of td's from a particular tr
    row_list.append(list_of_td)

for i in row_list:
    data.append(i)

df = pd.DataFrame(data, columns=['N0', 'state', 'Total_Confirmed_cases', 'Cured/Discharged', 'Death'])

df['Total_Confirmed_cases'] = pd.to_numeric(df['Total_Confirmed_cases'])
df['Cured/Discharged'] = pd.to_numeric(df['Cured/Discharged'])
df['Death'] = pd.to_numeric(df['Death'])

df.to_excel('corona_virus.xlsx', sheet_name='sheet1', index=False)

df = df.drop([0,33,34,35]) #deleting extras rows

#df[["Total confirmed cases"]]= df[["Total confirmed cases"]].apply(pd.to_numeric)
#df['Total_Confirmed_cases'] = df['Total_Confirmed_cases'].astype(int)

#________________showing top 5 cites data on graph______________________

top_cities=df.sort_values(by='Total_Confirmed_cases',ascending=False).head() #top 5 rows selected

labels = top_cities['state']
Total_Confirmed_cases = top_cities['Total_Confirmed_cases']
Death = top_cities['Death']
recorved = top_cities['Cured/Discharged']

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, Total_Confirmed_cases, width, label='Total Confirmed cases')
rects2 = ax.bar(x + width/2, Death, width, label='Death')
rects3 = ax.bar(x - width/2, recorved, width, label='Recorved cases')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Covid-19')
ax.set_title('Active cases, Deaths and Recorved patients')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

#styling graph
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
fig.tight_layout()

plt.show()
print("completed...")
