#dl latest data -
# curl https://raw.githubusercontent.com/CSSEGISandData/COVID-19//master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv --output covid.csv

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('covid.csv')
print(df.columns)
df = df.groupby('Country/Region',as_index=False).sum() #.unstack()
df = df[df.iloc[:,-1]>200]  # take countries w, > 200 cases by  now
cols = df.columns
for col in cols[3:]:
    df[col] = df[col].apply(lambda r:r if r>50  else np.NaN)

def plotter(dates,row):
    confirmed_cases = row[3:]
    indices = np.where(confirmed_cases>50)
    first_ind = indices[0][0]
    plt.plot(dates,confirmed_cases,'-o',label=row[0],markersize=3)

df.apply(lambda r: plotter(df.columns[3:],r),axis=1)
plt.legend(loc='upper left')
plt.yscale('log')
plt.xticks(rotation=70)
ax = plt.gca()
ax.xaxis.set_major_locator(plt.MaxNLocator(15))  #reduce ticks
last_date = df.columns[-1]
plt.title('Covid19 confirmed cases till {}'.format(last_date))
plt.show()
