#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import re
import json
import pandas as pd
import numpy as np
from scipy import stats
import warnings
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import plotly.express as px


# In[183]:


warnings.filterwarnings('ignore')
req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

## BUILD MULPIPLE CITY ANALYSIS
city = 'pleasantgrove-ut/' #*****change this city to what you want!!!!*****
data_list = []
urls = []
for page in range(1,15):
    if page == 1:
        url = 'https://www.zillow.com/homes/for_sale/'+city
    else:
        url = 'https://www.zillow.com/homes/for_sale/'+city+str(page)+'_p/'
    with requests.Session() as s:
        r = s.get(url, headers=req_headers)
        data = json.loads(re.search(r'!--(\{"queryState".*?)-->', r.text).group(1))
    urls.append(url)
    data_list.append(data)
    
df1 = pd.DataFrame()

def make_frame(frame):
    for i in data_list:
        for item in i['cat1']['searchResults']['listResults']:
            frame = frame.append(item, ignore_index=True)
    return frame

df1 = make_frame(df1)


# In[184]:


city = 'orem-ut/' #*****change this city to what you want!!!!*****
data_list = []
urls = []
for page in range(1,15):
    if page == 1:
        url = 'https://www.zillow.com/homes/for_sale/'+city
    else:
        url = 'https://www.zillow.com/homes/for_sale/'+city+str(page)+'_p/'
    with requests.Session() as s:
        r = s.get(url, headers=req_headers)
        data = json.loads(re.search(r'!--(\{"queryState".*?)-->', r.text).group(1))
    urls.append(url)
    data_list.append(data)
    
df2 = pd.DataFrame()

def make_frame(frame):
    for i in data_list:
        for item in i['cat1']['searchResults']['listResults']:
            frame = frame.append(item, ignore_index=True)
    return frame

df2 = make_frame(df2)


# In[185]:


city = 'provo-ut/' #*****change this city to what you want!!!!*****
data_list = []
urls = []
for page in range(1,15):
    if page == 1:
        url = 'https://www.zillow.com/homes/for_sale/'+city
    else:
        url = 'https://www.zillow.com/homes/for_sale/'+city+str(page)+'_p/'
    with requests.Session() as s:
        r = s.get(url, headers=req_headers)
        data = json.loads(re.search(r'!--(\{"queryState".*?)-->', r.text).group(1))
    urls.append(url)
    data_list.append(data)
    
df3 = pd.DataFrame()

def make_frame(frame):
    for i in data_list:
        for item in i['cat1']['searchResults']['listResults']:
            frame = frame.append(item, ignore_index=True)
    return frame

df3 = make_frame(df3)


# In[186]:


df = pd.concat([df1,df2,df3])
df


# In[188]:


#filter unneccesary columns
df = df.drop('hdpData', 1) #remove this line to see a whole bunch of other random cols, in dict format

#get rid of duplicates
df = df.drop_duplicates(subset='zpid', keep="last")
df['area'] = df['area'].fillna(1)
#filters
df['zestimate'] = df['zestimate'].fillna(0)
df['best_deal'] = df['unformattedPrice'] - df['zestimate']
df['price per sq ft'] = df['unformattedPrice'] / df['area']

print('shape:', df.shape)
homes = df[['address','beds','baths','area','price','zestimate','best_deal', 'price per sq ft','unformattedPrice']]


# In[189]:


homes['city'] = homes['address'].str.split(',')
homes['city'] = homes['city'].str[1]
homes = homes.sort_values(by='price',ascending=True)


# In[190]:


homes


# In[143]:


## READ TO CSV FILE

# compression_opts = dict(method='zip',
#                         archive_name='slchomes_10_19.csv')  
# homes.to_csv('slchomes_10_19.zip', index=False,
#           compression=compression_opts) 


# In[144]:


# make a price range column??? For color as well...

# homesnona = homes.dropna()
# import plotly.express as px
# fig = px.scatter(homesnona, x="beds", y="baths", size = 'area',
#                 hover_data=['price'], color = 'price')
# fig.show()


# In[191]:


df = homes
df['beds'] = df['beds'].astype(float)
df['baths'] = df['baths'].astype(float)
print(df.dtypes)


# In[192]:


df.describe(include='all')


# In[193]:


df.isnull().sum()


# In[194]:


plt.subplot(221)
df['beds'].value_counts().plot(kind='bar', title='Bedrooms/House', figsize=(16,9))
plt.xticks(rotation=0)
plt.xlabel('Bedrooms')
plt.ylabel('Quantity of Homes')

plt.subplot(222)
df['baths'].value_counts().plot(kind='bar', title='Baths/House')
plt.xticks(rotation=0)
plt.xlabel('Bathrooms')
plt.ylabel('Quantity of Homes')

# plt.subplot(223)
# df['lunch'].value_counts().plot(kind='bar', title='Lunch status of students')
# plt.xticks(rotation=0)

# plt.subplot(224)
# df['test preparation course'].value_counts().plot(kind='bar', title='Test preparation course')
# plt.xticks(rotation=0)

plt.show()


# In[195]:


sns.distplot(df['area'])


# In[196]:


corr = df[['baths','beds','unformattedPrice']].corr()
sns.heatmap(corr, annot=True, square=True)
plt.yticks(rotation=0)
plt.show()


# In[197]:


sns.relplot(x='baths', y='beds', data=df)


# In[198]:


sns.relplot(x='best_deal', y='unformattedPrice', data=df)


# In[199]:


df = df[(np.abs(stats.zscore(df['unformattedPrice'])) < 3)]
sns.relplot(x='best_deal', y='unformattedPrice', data=df)


# In[200]:


homes['bedbathratio'] = homes['beds'] / homes['baths']


# In[201]:


homes


# In[222]:


homes1 = homes.sort_values(by=['unformattedPrice'], ascending=True)
fig = px.violin(homes1, box = True, y = 'price', x = 'city')

fig.show()


# In[223]:


df4 = homes.loc[(homes['city'] == ' Provo') | (homes['city'] == ' Orem') 
                | (homes['city'] == ' Vineyard') | (homes['city'] == ' Pleasant Grove') 
                | (homes['city'] == ' American Fork') | (homes['city'] == ' Spanish Fork')]


# In[227]:


df4 = df4.sort_values(by=['unformattedPrice'], ascending=True)
fig = px.violin(df4, box = True, y = 'price', x = 'city', width = 1000)
fig.show()


# In[ ]:




