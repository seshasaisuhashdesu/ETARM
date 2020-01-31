#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
import collections as c


# In[ ]:


def consequent(self):
    def __init__(self):
        


# In[8]:


data = pd.read_csv(r'Documents/DataMining_Paper/Datasets/chess.txt',sep=" ",header=None)
data.head()


# In[9]:


data.drop(37,axis=1,inplace=True)
data.head()


# In[64]:


itemset = list(set(data.values.flatten()))


# In[ ]:





# In[65]:


tidsets=[[]]
for i in itemset:
    tidsets.append([])
for i in range(len(data)):
    for j in range(len(data.columns)):
        val = data.iloc[i][j]
        tidsets[val-1].append(i)
tidsets


# In[1]:


temp=tidsets


# In[ ]:





# In[ ]:





# In[57]:


#[j for j in range(len(data)) if max((data==itemset[0]).iloc[j])==True]
data.iloc[0].values


# In[ ]:


for i in itemset:
    for j in data


# In[ ]:





# In[16]:


minsup=0
minconf=0.8
k=1000


# In[31]:


itemcount = dict(c.Counter(data.values.flatten()))


# In[ ]:


def save(item1,item2,L,k,minsup):
    
    


# In[32]:


items = list(itemcount.keys())
for i in range(len(items)):
    for j in range(i+1,len(items)):
        if itemcount[items[i]]>minsup and itemcount[items[j]]>minsup:
            if confidence(items[i],items[j])>minconf:
                save(items[i],items[j],L,k,minsup)
            if confidence(items[j],items[i])>minconf:
                save(items[j],items[i],L,k,minsup)
            


# In[36]:


max(['za','bc'])


# In[ ]:





# In[ ]:




