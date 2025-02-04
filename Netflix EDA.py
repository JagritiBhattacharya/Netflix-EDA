#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')


# In[2]:


df=pd.read_csv('/Users/jagritibhattacharya/netflix_titles.csv')
print(df.head(3))


# In[4]:


df.shape


# In[5]:


df.info()


# In[9]:


#Changing the date added column to object data type

df['date_added']=df['date_added'].str.strip()
df['date_added']=pd.to_datetime(df['date_added'],format='%B %d,%Y',errors='coerce')


# In[10]:


df.info()


# In[11]:


df.isnull().sum()


# In[3]:


df.nunique()


# In[4]:


#data cleaning

df=df.dropna(how='any',subset=['cast','director'])


# In[7]:


#replacing null values with 'missing'

df['country'].fillna('M(issing',inplace=True)
df['date_added'].fillna('Missing',inplace=True)
df['rating'].fillna('Missing',inplace=True)
df['duration'].fillna('Missing',inplace=True)
df.isnull().sum().sum()


# In[8]:


df.isnull().sum()


# In[10]:


#Coverting into proper date-Time format and adding month and year feature

df["date_added"]=pd.to_datetime(df['date_added'])
df['year_added']=df['date_added'].dt.year
df['month_added']=df['date_added'].dt.month

# df


# In[11]:


#renaming the listed_in feature to  genre 

df=df.rename(columns={"listed_in":"genre"})
df['genre']=df['genre'].apply(lambda x:x.split(",")[0])
df.head()


# In[17]:


#Data Visualization


#Heatmap

# Heatmap
# Correlation between the feature show with the help of visualisation
corrs = df.corr()
fig_heatmap = ff.create_annotated_heatmap(
    z=corrs.values,
    x=list(corrs.columns),
    y=list(corrs.index),
    annotation_text=corrs.round(2).values,
    showscale=True)
fig_heatmap.update_layout(title= 'Correlation of whole Data',  
                          plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
                          title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                          font=dict(color='#8a8d93'))


# In[18]:


fig_donut = px.pie(df, names='type', height=300, width=600, hole=0.7,

title='Most watched on Netflix',

color_discrete_sequence=['#b20710', '#221f1f'])

fig_donut.update_traces(hovertemplate=None, textposition='outside',

textinfo='percent+label', rotation=90)

fig_donut.update_layout(margin=dict(t=60, b=30, l=0, r=0), showlegend=False,

plot_bgcolor='#333', paper_bgcolor='#333',

title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))


# In[19]:


df_rating = pd.DataFrame(df['rating'].value_counts()).reset_index().rename(columns={'index':'rating','rating':'count'})

fig_bar = px.bar(df_rating, y='rating', x='count', title='Distribution of Rating',

color_discrete_sequence=['#b20710'], text='count')

fig_bar.update_xaxes(showgrid=False)

fig_bar.update_yaxes(showgrid=False, categoryorder='total ascending', ticksuffix=' ', showline=False)

fig_bar.update_traces(hovertemplate=None, marker=dict(line=dict(width=0)))

fig_bar.update_layout(margin=dict(t=80, b=0, l=70, r=40),

hovermode="y unified",

xaxis_title=' ', yaxis_title=" ", height=400,

plot_bgcolor='#333', paper_bgcolor='#333',

title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),

font=dict(color='#8a8d93'),

legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),

hoverlabel=dict(bgcolor="black", font_size=13, font_family="Lato, sans-serif")) 


# In[22]:


df_month=pd.DataFrame(df.month_added.value_counts()).reset_index().rename(
columns={'index':'month','month_added':'count'})

df_month['month_final'] = df_month['month'].replace({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'June', 7:'July', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'})
df_month[:2]


# In[26]:


d2 = df[df["type"] == "Movie"]
d2[:2]


# In[27]:


col ='year_added'

vc2 = d2[col].value_counts().reset_index().rename(columns = {col : "count", "index" : col})

vc2['percent'] = vc2['count'].apply(lambda x : 100*x/sum(vc2['count']))

vc2 = vc2.sort_values(col)

vc2[:3]


# In[23]:


fig_month = px.funnel(df_month, x='count', y='month_final', title='Best month for releasing Content',
                      height=350, width=600, color_discrete_sequence=['#b20710'])
fig_month.update_xaxes(showgrid=False, ticksuffix=' ', showline=True)
fig_month.update_traces(hovertemplate=None, marker=dict(line=dict(width=0)))
fig_month.update_layout(margin=dict(t=60, b=20, l=70, r=40),
                        xaxis_title=' ', yaxis_title=" ",
                        plot_bgcolor='#333', paper_bgcolor='#333',
                        title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),
                        font=dict(color='#8a8d93'),
                        hoverlabel=dict(bgcolor="black", font_size=13, font_family="Lato, sans-serif"))


# In[24]:


df_genre = pd.DataFrame(df.genre.value_counts()).reset_index().rename(columns={'index':'genre', 'genre':'count'})
fig_tree = px.treemap(df_genre, path=[px.Constant("Distribution of Geners"), 'count','genre'])
fig_tree.update_layout(title='Highest watched Geners on Netflix',
                  margin=dict(t=50, b=0, l=70, r=40),
                  plot_bgcolor='#333', paper_bgcolor='#333',
                  title_font=dict(size=25, color='#fff', family="Lato, sans-serif"),
                  font=dict(color='#8a8d93'),
                  hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))


# In[28]:


#Comparison Yoy 

fig1 = go.Figure(go.Waterfall(
    name = "Movie", orientation = "v", 
    x = vc2['year_added'].values,
    textposition = "auto",
    text = ["1", "2", "1", "13", "3", "6", "14", "48", "204", "743", "1121", "1366", "1228", "84"],
    y = [1, 2, -1, 13, -3, 6, 14, 48, 204, 743, 1121, 1366, -1228, -84],
    connector = {"line":{"color":"#b20710"}},
    increasing = {"marker":{"color":"#b20710"}},
    decreasing = {"marker":{"color":"orange"}},
))
fig1.show()


# In[ ]:




