#!/usr/bin/env python
# coding: utf-8

# In[62]:


import matplotlib.pyplot as plt
import pandas as pd
import july
from july.utils import date_range


# In[63]:


df = pd.read_csv('Crimedata.csv')
T = df['CrimeDateTime']  


# Fill nan data with next value
T.fillna(method='backfill', inplace=True)

# check and remove nan
T = [x for x in T if x == x]


# In[64]:


# split date and time
for i in range(len(T)):
    T[i] = T[i].split()
    T[i] = T[i][0]
# print(T[:10])


# count incident # each day
Incident = {}
for i in T:
    if i not in Incident:
        Incident[i]=1
    else:
        Incident[i]+=1


# In[68]:


# extract the daily crime on specific year and month

# def yearmth(year,month):
#     num = []
#     target = year + "/" + month
#     for k,v in Incident.items():
#         ym = k[0:7]
#         if target == ym:
#             num.append(v)
#     return num

def yearCrime(year):
    num = []
    target = year
    for k,v in Incident.items():
        ym = k[0:4]
        if target == ym:
            num.append(v)
    return num


# In[69]:


# set up for dropdown
year = '2016'
mth = '05'

start = year + "-01-01"
end = year + "-12-31"

dates = date_range(start,end) # datetime
num = yearCrime(year) # number of incidenet

# print(num)


# In[70]:


# plot whole year calendar
july.calendar_plot(dates, num)


# In[72]:


# plot one year calendar
july.month_plot(dates, num, month=int(mth), colorbar=True)


# In[ ]:




