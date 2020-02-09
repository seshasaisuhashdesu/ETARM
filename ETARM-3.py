#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import collections as c
import numpy as np
import heapq


# In[2]:


class RuleData:
    def __init__(self,rule=((),()) ,support=0.0, confidence=0.0, expFlag=True):
        self.rule=rule
        self.support=support
        self.confidence=confidence
        self.expFlag=expFlag
    def __lt__(self,r):
        return self.support<r.support
    def __str__(self):
        return str(str(self.rule), str(self.support), str(self.confidence), str(self.expFlag))


# In[3]:


#data = pd.read_csv(r'Datasets/chess.txt',sep=" ",header=None)
data = pd.read_csv(r'Datasets/sample.txt',sep=" ",header=None)
data.head()

itemset = list(set(data.values.flatten()))
itemset


# In[6]:


tidsets={}
for i in range(len(data)):
    for j in range(len(data.columns)):
        val = data.iloc[i][j]
        if pd.notna(val):
            if val in tidsets:
                tidsets[val].append(i)
            else:
                tidsets[val]=[i]
tidsets


# In[8]:


#[j for j in range(len(data)) if max((data==itemset[0]).iloc[j])==True]
data.iloc[0].values


# In[9]:


minsup=0
minconf=0.8
k=10


# In[11]:


class MyHeap:
    def __init__(self, initial=None, key=lambda x:x):
        self.key = key
        self._data = []
        if initial:
                self._data = [(self.key(item), item) for item in initial]
                heapq.heapify(self._data)

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), item))

    def pop(self):
        return heapq.heappop(self._data)[1]
    def length(self):
        return len(self._data)
    def __str__(self):
        return str(self._data)


# In[12]:


def support(rule=((),())):
    '''if(isinstance(rule[0],int) or isinstance(rule[0],float)):
        if(isinstance(rule[1],int) or isinstance(rule[1],float)):
            rule=[[rule[0]],[rule[1]]]
        elif(isinstance(rule[1],tuple)):
            rule=[[rule[0]],list(rule[1])]
    elif(isinstance(rule[1],int) or isinstance(rule[1],float)):
        if(isinstance(rule[0],tuple)):
            rule=[list(rule[0]), [rule[1]]]'''
    items=rule[0]+rule[1]
    sumRule=0
    for i in range(len(data)):
        flagRule=True
        for j in items:
            if j not in list(data.iloc[i,:]):
                flagRule=False
                break
        if(flagRule):
            sumRule+=1
    return sumRule/len(data)


# In[14]:


def confidence(rule=((),())):
    #print(rule)
    '''if(isinstance(rule[0],int) or isinstance(rule[0],float)):
        if(isinstance(rule[1],int) or isinstance(rule[1],float)):
            rule=[[rule[0]],[rule[1]]]
        elif(isinstance(rule[1],tuple)):
            rule=[[rule[0]],list(rule[1])]
    elif(isinstance(rule[1],int) or isinstance(rule[1],float)):
        if(isinstance(rule[0],tuple)):
            rule=[list(rule[0]), [rule[1]]]'''
    items=rule[0]+rule[1]
    #print(rule)
    #print(items)
    sumRule=0
    sumAntecedant=0
    #The following can be optimized by bringing both under single loop block
    for i in range(len(data)):
        flagRule=True
        for j in items:
            if j not in list(data.iloc[i,:]):
                flagRule=False
                break
        if(flagRule):
            sumRule+=1
            
    for i in range(len(data)):
        flagAntecedant=True
        for j in rule[0]:
            if j not in list(data.iloc[i,:]):
                flagAntecedant=False
                break
        if(flagAntecedant):
            sumAntecedant+=1
            
    return sumRule/sumAntecedant


# In[15]:


ruleDetails=dict()
L=MyHeap(key=lambda x:-x.support)


# In[22]:


def save(L,k,sup,conf,expandSide,rule=((),())):
    global minsup
    print(minsup)
    '''if(isinstance(rule[0],int) or isinstance(rule[0],float)):
        if(isinstance(rule[1],int) or isinstance(rule[1],float)):
            rule=[[rule[0]],[rule[1]]]
        elif(isinstance(rule[1],tuple)):
            rule=[[rule[0]],list(rule[1])]
    elif(isinstance(rule[1],int) or isinstance(rule[1],float)):
        if(isinstance(rule[0],tuple)):
            rule=[list(rule[0]), [rule[1]]]'''
    expFlag=True
    if(max(rule[0])==largestElement and expandSide=="left"):
        expFlag=False
    elif(max(rule[1])!=largestElement and expandSide=="right"):
        expFlag=False
    L.push(RuleData(rule,sup,conf,expFlag))
    ruleDetails[rule]=sup 
    if(expFlag):
        R.push(RuleData(rule,sup,conf,expFlag))
    ruleData=RuleData()
    q=list()
    flag=False
    for i in range(min(L.length(),k)):
        q+=[L.pop()]
        flag=True
    if(L.length()>0):
        ruleData=L.pop()
        while(ruleData.support==q[-1].support):
            q+=[ruleData]
            if(L.length()>0):
                ruleData=L.pop()
            else:
                break
    
        
    if(not flag):
        return L
    else:
        minsup=q[-1].support
        return MyHeap(q, key=lambda x:-x.support) 


# In[23]:


largestElement=max(tidsets.keys())


# In[24]:


R=MyHeap(key=lambda x:-x.support)


# In[25]:


items = list(tidsets.keys())
print(items)
for i in range(len(items)):
    for j in range(i+1,len(items)):
        if len(tidsets[items[i]])/len(data)>=minsup and len(tidsets[items[j]])/len(data)>=minsup:
            
            conf1=confidence(((items[i],),(items[j],)))
            conf2=confidence(((items[j],),(items[i],)))
            if conf1>=minconf:
                #ruleDetails[(items[i],items[j])]=support(((items[i],),(items[j],)))
                #print(conf1)
                #print(((items[i],),(items[j],)))
                #L = save(L,k,ruleDetails[(items[i],items[j])],conf1,((items[i],),(items[j],)))
                L = save(L,k,support(((items[i],),(items[j],))),conf1,"left",((items[i],),(items[j],)))
            if conf2>=minconf:
                #ruleDetails[(items[j],items[i])]=support(((items[j],),(items[i],)))
                #print(conf2)
                #print(((items[j],),(items[i],)))
                #L = save(L,k,ruleDetails[(items[j],items[i])],conf2,((items[j],),(items[i],)))
                L = save(L,k,support(((items[j],),(items[i],))),conf2,"left",((items[j],),(items[i],)))
                


# In[26]:

print("L with expand flags after step 1")
for i in L._data:
    print(i[1].support,i[1].rule,i[1].expFlag)


# In[27]:


L._data


# In[28]:


data


# In[29]:


def ExpandL(ruleData,L,R,k):
    candidateItems=set()
    rule=ruleData.rule;
    items=set(list(rule[0])+list(rule[1]))
    for i in range(len(data)):
        flag=True
        for j in items:
            if j not in data.iloc[i,:]:
                flag=False
        if(flag):
            for x in data.iloc[i,:]:
                if x not in items and x>max(rule[0]):
                    candidateItems.add(x)
    for c in candidateItems:
        rnew=(ruleData.rule[0]+(c,), ruleData.rule[1])
        sup=support(rnew)
        if  sup>=minsup:
            conf=confidence(rnew)
            if conf>=minconf:
                #print(L, "HELLO")
                L=save(L,k,sup,conf,"left",rnew)
    return L


# In[30]:


def ExpandR(ruleData,L,R,k):
    candidateItems=set()
    rule=ruleData.rule;
    items=set(list(rule[0])+list(rule[1]))
    for i in range(len(data)):
        flag=True
        for j in items:
            if j not in data.iloc[i,:]:
                flag=False
        if(flag):
            for x in data.iloc[i,:]:
                if x not in items and x>max(rule[1]):
                    candidateItems.add(x)
    for c in candidateItems:
        rnew=(ruleData.rule[0], ruleData.rule[1]+(c,))
        sup=support(rnew)
        if  sup>=minsup:
            conf=confidence(rnew)
            if conf>=minconf:
                L=save(L,k,sup,conf,"right",rnew)
    return L


# In[31]:


while(R.length()!=0):
    ruleData=R.pop()
    if ruleData.support>=minsup:
        if(ruleData.expFlag):
            L=ExpandL(ruleData,L,R,k)
            L=ExpandR(ruleData,L,R,k)
        else:
            L=ExpandR(ruleData, L, R, k)
    q=list()
    flag=False
    if R.length()>0:
        ruleData=R.pop()
        while(ruleData.support>=minsup and R.length()>0):
            q+=[ruleData]
            ruleData=R.pop()
            flag=True
    if(flag):
        R =  MyHeap(q,lambda x:-x.support)


# In[35]:
print()
print("Support\tConfidence\tRule")
for i in L._data:
    print(round(i[1].support,2),"\t", round(i[1].confidence,2),"\t\t", i[1].rule)

