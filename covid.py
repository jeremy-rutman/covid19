#dl latest data -
# curl https://raw.githubusercontent.com/CSSEGISandData/COVID-19//master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv --output covid.csv

# curl https://raw.githubusercontent.com/CSSEGISandData/COVID-19//master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import itertools

def plotter(dates,row):
    confirmed_cases = row[3:]
    indices = np.where(confirmed_cases>50)
    first_ind = indices[0][0]
    plt.plot(dates,confirmed_cases,'-o',label=row[0],markersize=3)

def plotter_promil(row):
    colnames = list(row.index)
    end_of_dates = colnames.index('index')
    print('end fo dates',end_of_dates)
    offset = 30

    confirmed_cases = row[3+offset:end_of_dates]
    last_death = row[end_of_dates-1]
    # print('row',row)
    # print('row',row.index)
    pop = row['population']
    pop = int(pop)/(10**6)
    print(pop,row['Country/Region'])
    print(last_death,last_death/pop)
    indices = np.where(confirmed_cases>50)
    plt.plot(row.index[3+offset:end_of_dates],confirmed_cases/pop,marker=next(marker), label=row[0],markersize=5)

marker = itertools.cycle(( '+', '.', 'o','v','^', '*','<','>','s','p','D'))

df = pd.read_csv('test.csv',sep=',')
print(df.columns)
df = df.groupby('Country/Region',as_index=False).sum() #.unstack()
df = df[df.iloc[:,-1]>500]  # take countries w, > 200 cases by  now
cols = df.columns
for col in cols[3:]:
    df[col] = df[col].apply(lambda r:r if r>50  else np.NaN)


#df_country_pops = pd.read_excel('world_pops.xlsx')
df_country_pops = pd.read_csv('world_pops.csv',sep=',')
print(df_country_pops.columns[0:20])


df_all = pd.merge(df,df_country_pops,how='left',left_on='Country/Region',right_on='country')
# print(len(df),len(df_country_pops),len(df_all))
# for i in range(5):
#     print(df_all.iloc[i,:])
# #print(df_all.head().T)    #df.join(df_country_pops,on='')

print(df_all[df_all['Country/Region']=='China'])
print(df_all[df_all['Country/Region']=='US'])
print(df_all.tail(10))

df_all.apply(lambda r: plotter_promil(r),axis=1)
#plt.legend(fontsize='small') #loc='upper left',
#plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.1)
plt.legend(bbox_to_anchor=(1.05, 1))
#plt.yscale('log')
plt.xticks(rotation=70)
ax = plt.gca()
ax.xaxis.set_major_locator(plt.MaxNLocator(15))  #reduce ticks
last_date = df.columns[-1]
plt.title('Covid19 deaths per million {}'.format(last_date))
fig = plt.gcf()
fig.tight_layout()
plt.show()
