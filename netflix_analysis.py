#!/usr/bin/env python
# coding: utf-8

# In[29]:

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# In[8]:


netflix=pd.read_csv("netflix.csv")


# In[9]:


netflix


# In[10]:


netflix.shape #to find how manay row and coloumn


# In[12]:


netflix.info() # tell us all about the dataset


# In[14]:


netflix.isnull().sum()


# In[16]:


netflix.describe() # to find satatical value to describe


# In[ ]:


netflix = netflix.fillna(netflix.median(numeric_only=True))


# In[19]:


netflix.duplicated().sum()


# In[21]:


netflix.drop_duplicates()


# In[22]:


netflix['Watch_Date']=pd.to_datetime(netflix['Watch_Date'])


# In[23]:


netflix.dtypes


# In[32]:


#DATA ANSLYSIS# 
netflix.groupby("Region")["Monthly_Revenue"].sum().plot(kind='bar', ylabel='Month_revenue', title='Region wise Revenue')


# In[38]:


netflix.groupby("Subscription_Plan")["Rating"].sum().plot(kind='pie',title='Subscription_plan wise Rating')


# In[39]:


netflix.groupby("Category")["Monthly_Revenue"].sum().plot(kind='bar', ylabel='Month_revenue', title='Category wise Revenue')


# In[43]:


netflix['month']=netflix['Watch_Date'].dt.month_name()


# In[44]:


netflix


# In[47]:


netflix.groupby("month")["Monthly_Revenue"].sum().plot(kind='bar', ylabel='Month_revenue', title='Month wise Revenue')


# In[ ]:




