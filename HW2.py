#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 17:29:16 2022

@author: kali
"""

#%% imports
import pandas as pd
import re
import numpy as np
from matplotlib.pyplot import hist
import matplotlib.pyplot as plt
from urllib.parse import urlparse


#%% read in data

aiml_data = pd.read_csv('Downloads/reddit_database.csv')

aiml_data.head()

#%% basic info about data
aiml_data.info()
aiml_data.describe()

#%% convert date 

aiml_data['author_created_date'] = pd.to_datetime(aiml_data['author_created_utc'], unit='s')

aiml_data['created_date'] = pd.to_datetime(aiml_data['created_date'])


aiml_data.info()

aiml_data.describe(include="all", datetime_is_numeric=True)

#%% get the day of the week

aiml_data['dow'] = aiml_data['created_date'].dt.day_name()

#%% 1.1 Count number of posts by subreddit
subreddit_count = aiml_data['subreddit'].str.lower().str.split(expand=True).stack().value_counts()

subreddit_count = subreddit_count.head()
print(subreddit_count)

#%% 1.2 count number of posts by user
user_post_count= aiml_data['author'].str.lower().str.split(expand=True).stack().value_counts()

user_post_count = user_post_count.head()
print (user_post_count.head)

#%% 1.3 number of unique authors per subreddit
unique_authors  = aiml_data.groupby('subreddit')['author'].describe()
print(unique_authors.sort_values(by='unique', ascending=False).head())

#%% 1.4 percentage of posts have value

percent_posts = aiml_data.groupby('subreddit')['post'].describe(include=all)
print(percent_posts.sort_values(by='unique', ascending=False))
"""
 -------------------- Question 2 ----------------------------------------------
 """
 
 
 #%%2.1 line graph with posts over time
 
post_plot = aiml_data.groupby('created_date')['title'].count().plot(kind='line')

post_plot.set(xlabel="Date_created", ylabel="Total Number of Posts",
             title="Total number of posts over time")

post_plot.get_figure()

#%% 2.2 histogram by scores

hist_scores= aiml_data['score'].plot(kind='hist', range=[0,20])
hist_scores.set(xlabel="Scores", ylabel="Posts", title="Distribution of Post Scores")
hist_scores.get_figure()


#%% 2.3 day of week plot

dow_plot = aiml_data.groupby('dow')['created_date'].count().plot(kind='bar')

dow_plot.set(xlabel="Day Of The Week", ylabel="Total Number of Posts",
             title="Total Posts Per day of the week")

dow_plot.get_figure()

#%% 2.4 hour of day plot

aiml_data['hour'] = aiml_data['created_date'].dt.hour
hod_plot = aiml_data.groupby('hour')['created_date'].count().plot(kind='bar')
hod_plot.set(xlabel = "Hour of The Day", ylabel="Posts")

"""
----------------------------Question 3 ----------------------------------------

"""

#%% 3.1 New posts- 30 days
    from datetime import timedelta, datetime
lastday = pd.to_datetime('6/8/2021')
aiml_data['dates'] = aiml_data['author_created_date'].dt.date
L = aiml_data.sort_index(ascending=False)
I = L[L["created_date"] >= (pd.to_datetime(lastday) - pd.Timedelta(days=30))]
print(I.groupby('subreddit').describe().head(5))

#%% 3.2 length of post, score

aiml_data['title_words'] = aiml_data['title'].str.count(' ')
score_length= aiml_data.groupby('title_words')['score'].count().plot()
score_length.set(xlabel="Title Word Count", ylabel="Scores",
             title="Scores/Title Word Count")



#%% 3.3 top words in post titles

title_words = aiml_data['title'].str.lower().str.split(expand=True).stack().value_counts()

title_words = title_words.head(20)
print(title_words)

#%% 3.4 most linked website domains

def sort_domains(text):
    domain = urlparse(text).netloc
    return domain
aiml_data['post_domains'] = aiml_data['title'].apply(sort_domains)
domain_count = aiml_data.groupby('post_domains').count()
print(domain_count.sort_values(by='title', ascending=False).head(10))

