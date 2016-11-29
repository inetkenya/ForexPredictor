
# coding: utf-8

# In[132]:

# import libs

import json
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import urllib.request  # for HTTP requests (web scraping, APIs)
from datetime import datetime, timedelta
import os
from dateutil import parser as dateparser


# ### Open JSON file with articles

# In[133]:

articles = pd.read_json('small_data.json')


# In[134]:

articles['created_at'] = articles.apply((lambda row: dateparser.parse(row.date[0])), axis=1)


# In[135]:

articles['updated_at'] = articles.apply((lambda row: dateparser.parse(row.date[1]) if len(row.date) > 1 else None), axis=1)


# In[136]:

articles


# In[137]:

concurancy_pair_path = "./EURUSD1.csv"
pair = pd.read_csv(concurancy_pair_path,
                   dtype = {'<TIME>': np.str, '<DTYYYYMMDD>': np.str}
                  )
pair.rename(columns={'<TICKER>': 'TICKER', 
                 '<DTYYYYMMDD>': 'DTYYYYMMDD', 
                 '<TIME>': 'TIME', 
                 '<OPEN>': 'OPEN',
                 '<HIGH>': 'HIGH',
                 '<LOW>': 'LOW',
                 '<CLOSE>': 'CLOSE',
                 '<VOL>': 'VOL'
                }, inplace=True)


# In[138]:

convert_date = (lambda row: datetime.strptime(str(row['DTYYYYMMDD'])+str(row['TIME']), '%Y.%m.%d%H:%M'))
pair['DATETIME'] = pair.apply(convert_date, axis=1)


# In[139]:

pair.tail(10)


# In[237]:

nearest_id = lambda row: int(((pair.DATETIME - row).abs() / np.timedelta64(1, 's')).argsort()[:1])


# In[238]:

articles['pair_id'] = articles.apply(lambda row: nearest_id(row.created_at.tz_convert(None)), axis=1)


# In[245]:

def next_nearest_id(row):
    this_date = pair.DATETIME[row.pair_id]
    next_id = nearest_id(this_date + np.timedelta64(1, 'D'))
    next_date = pair.DATETIME[next_id]
    return next_id if ((next_date - this_date) > np.timedelta64(20, 'h')) else None


# In[246]:

articles['next_pair_id'] = articles.apply(next_nearest_id, axis=1)


# In[259]:

def wow(row):
    if (row.next_pair_id > -1 and row.pair_id > -1):
        diff = (float(pair.OPEN[row.pair_id]) - float(pair.OPEN[int(row.next_pair_id)]))
        threshold = 2e-5
        step = 0 if (abs(diff) < threshold) else (-1 if (diff < 0) else 1)
        return step


# In[260]:

articles['direction'] = articles.apply(wow, axis=1)


# In[261]:

articles


# In[165]:

pair.DATETIME[65000]


# In[262]:

articles.to_csv('super.json')


# In[263]:

pd.read_csv('super.json')


# In[ ]:



