
# coding: utf-8

# Importing libraries

# In[49]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


# Scraping wikipedia page for Toronto table

# In[50]:


wiki_link = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
req = requests.get(wiki_link).text
soup = BeautifulSoup(req, 'lxml')


# In[51]:


table = soup.find('table')
print(table)

Postcode = []
Borough = []
Neighbourhood = []


# In[52]:


for tr_cell in table.find_all('tr'):
    
    counter = 1
    Postcode_var      = -1
    Borough_var       = -1
    Neighbourhood_var = -1
    
    for td_cell in tr_cell.find_all('td'):
        if counter == 1: 
            Postcode_var = td_cell.text
        if counter == 2: 
            Borough_var = td_cell.text
            tag_a_Borough = td_cell.find('a')
            
        if counter == 3: 
            Neighbourhood_var = str(td_cell.text).strip()
            tag_a_Neighbourhood = td_cell.find('a')
            
        counter +=1
        
    if (Postcode_var == 'Not assigned' or Borough_var == 'Not assigned' or Neighbourhood_var == 'Not assigned'): 
        continue
    try:
        if ((tag_a_Borough is None) or (tag_a_Neighbourhood is None)):
            continue
    except:
        pass
    if(Postcode_var == -1 or Borough_var == -1 or Neighbourhood_var == -1):
        continue
        
    Postcode.append(Postcode_var)
    Borough.append(Borough_var)
    Neighbourhood.append(Neighbourhood_var)


# In[53]:


unique_p = set(Postcode)

Postcode_u      = []
Borough_u       = []
Neighbourhood_u = []


for postcode_unique_element in unique_p:
    p_var = ''; b_var = ''; n_var = ''; 
    for postcode_idx, postcode_element in enumerate(Postcode):
        if postcode_unique_element == postcode_element:
            p_var = postcode_element;
            b_var = Borough[postcode_idx]
            if n_var == '': 
                n_var = Neighbourhood[postcode_idx]
            else:
                n_var = n_var + ', ' + Neighbourhood[postcode_idx]
    Postcode_u.append(p_var)
    Borough_u.append(b_var)
    Neighbourhood_u.append(n_var)


# In[54]:


toronto_dict = {'Postcode':Postcode_u, 'Borough':Borough_u, 'Neighbourhood':Neighbourhood_u}
df_toronto = pd.DataFrame.from_dict(toronto_dict)
df_toronto.head(14)

import geocoder
from geopy.geocoders import Nominatim


# In[55]:


nom = Nominatim(user_agent = None, timeout = 20)
df_toronto['Canada']= 'Canada'
df_toronto.head(10)


# In[56]:


df_toronto['Full Address']=df_toronto['Neighbourhood']+', '+df_toronto['Canada']
df_toronto.head(5)
df_toronto['Coordinates'] = df_toronto['Full Address'].apply(nom.geocode)
df_toronto['Latitude']=df_toronto['Coordinates'].apply(lambda x: x.latitude if x!=None else None)
df_toronto['Longitude'] = df_toronto['Coordinates'].apply(lambda x: x.longitude if x!=None else None)


# In[57]:


df_toronto.head(10)


# In[58]:


df_toronto2 = df_toronto["Neighbourhood"].str.split(",", n = 1, expand = True)
df_toronto['First Address']=df_toronto2[0]
df_toronto['Final Address'] = df_toronto['First Address'] + ', '+df_toronto['Canada']
df_toronto['Coordinates2'] = df_toronto['Final Address'].apply(nom.geocode)
df_toronto['Lat']=df_toronto['Coordinates2'].apply(lambda x: x.latitude if x!=None else None)
df_toronto['Long'] = df_toronto['Coordinates2'].apply(lambda x: x.longitude if x!=None else None)


# In[59]:


print(df_toronto2.isnull().sum())


# In[60]:


df_toronto.head(10)


# In[61]:


df_toronto.isna().sum()


# In[62]:


print(df_toronto)


# In[63]:


df_toronto.iloc[29:54, :]


# In[64]:


df_toronto.iloc[30,11] = nom.geocode('Thistletown, Canada').latitude


# In[65]:


df_toronto.iloc[30]


# In[66]:


df_toronto.iloc[30,12] = nom.geocode('Thistletown, Canada').longitude


# In[67]:


df_toronto.iloc[30,:]


# In[68]:


df_toronto.iloc[60:62,:]


# In[69]:


df_toronto.iloc[61,11] = nom.geocode('Canadian Forces Base, Toronto, Canada').latitude


# In[70]:


df_toronto.iloc[61,:]


# In[71]:


df_toronto.iloc[61, 12] = nom.geocode('Canadian Forces Base, Toronto, Canada').longitude


# In[72]:


df_toronto.iloc[61,:]


# In[73]:


df_toronto.isna().sum()


# In[74]:


df_toronto.columns


# In[75]:


df_toronto_fin = df_toronto.iloc[:,[2,0,1,11,12]]


# In[76]:


df_toronto_fin.head(10)


# In[77]:


df_toronto_fin = df_toronto_fin.rename(index = str, columns = {'Lat':'Latitude', 'Long': 'Longitude'})


# In[78]:


df_toronto_fin.head(10)

