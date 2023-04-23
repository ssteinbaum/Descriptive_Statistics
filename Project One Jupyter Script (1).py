
# coding: utf-8

# # Project One: Data Visualization, Descriptive Statistics, Confidence Intervals
# 
# 
# You are a data analyst for a basketball team and have access to a large set of historical data that you can use to analyze performance patterns. The coach of the team and your management have requested that you use descriptive statistics and data visualization techniques to study distributions of key performance metrics that are included in the data set. These data-driven analytics will help make key decisions to improve the performance of the team. You will use the Python programming language to perform the statistical analyses and then prepare a report of your findings to present for the team’s management. Since the managers are not data analysts, you will need to interpret your findings and describe their practical implications. 
# 
# 

# The ELO rating, represented by the variable **elo_n**, is used as a measure of the relative skill of a team. This measure is inferred based on the final score of a game, the game location, and the outcome of the game relative to the probability of that outcome. The higher the number, the higher  the relative skill of a team.
# 
# 
# In addition to studying data on your own team, your management has assigned you a second team so that you can compare its performance with your own team's. 

# ## Step 1: Data Preparation & the Assigned Team
# 
# In[1]:


import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt
from IPython.display import display, HTML

nba_orig_df = pd.read_csv('nbaallelo.csv')
nba_orig_df = nba_orig_df[(nba_orig_df['lg_id']=='NBA') & (nba_orig_df['is_playoffs']==0)]
columns_to_keep = ['game_id','year_id','fran_id','pts','opp_pts','elo_n','opp_elo_n', 'game_location', 'game_result']
nba_orig_df = nba_orig_df[columns_to_keep]

# The dataframe for the assigned team is called assigned_team_df. 
# The assigned team is the Chicago Bulls from 1996-1998.
assigned_years_league_df = nba_orig_df[(nba_orig_df['year_id'].between(1996, 1998))]
assigned_team_df = assigned_years_league_df[(assigned_years_league_df['fran_id']=='Bulls')]
assigned_team_df = assigned_team_df.reset_index(drop=True)

display(HTML(assigned_team_df.head().to_html()))
print("printed only the first five observations...")
print("Number of rows in the data set =", len(assigned_team_df))


#  

# ## Step 2: Pick Your Team

# In[2]:


# Range of years: 2013-2015 (Note: The line below selects ALL teams within the three-year period 2013-2015. This is not your team's dataframe.
your_years_leagues_df = nba_orig_df[(nba_orig_df['year_id'].between(2013, 2015))]

# The dataframe for your team is called your_team_df.

your_team_df = your_years_leagues_df[(your_years_leagues_df['fran_id']=='Hawks')]
your_team_df = your_team_df.reset_index(drop=True)

display(HTML(your_team_df.head().to_html()))
print("printed only the first five observations...")
print("Number of rows in the data set =", len(your_team_df))


#  

# ## Step 3: Data Visualization: Points Scored by Your Team
# The coach has requested that you provide a visual that shows the distribution of points scored by your team in the years 2013-2015. 
#
# In[3]:


import seaborn as sns

# Histogram
fig, ax = plt.subplots()
plt.hist(your_team_df['pts'], bins=20)
plt.title('Histogram of points scored by Your Team in 2013 to 2015', fontsize=18)
ax.set_xlabel('Points')
ax.set_ylabel('Frequency')
plt.show()
print("")

# Scatterplot
plt.title('Scatterplot of points scored by Your Team in 2013 to 2015', fontsize=18)
sns.regplot(your_team_df['year_id'], your_team_df['pts'], ci=None)
plt.show()


#  

# ## Step 4: Data Visualization: Points Scored by the Assigned Team
# The coach has also requested that you provide a visual that shows a distribution of points scored by the Bulls from years 1996-1998. 
# In[4]:


import seaborn as sns

# Histogram
fig, ax = plt.subplots()
plt.hist(assigned_team_df['pts'], bins=20)
plt.title('Histogram of points scored by the Bulls in 1996 to 1998', fontsize=18)
ax.set_xlabel('Points')
ax.set_ylabel('Frequency')
plt.show()

# Scatterplot
plt.title('Scatterplot of points scored by the Bulls in 1996 to 1998', fontsize=18)
sns.regplot(assigned_team_df['year_id'], assigned_team_df['pts'], ci=None)
plt.show()


#  

# ## Step 5: Data Visualization: Comparing the Two Teams
# Now the coach wants you to prepare one plot that provides a visual of the differences in the distribution of points scored by the assigned team and your team. 
# 
# In[5]:


import seaborn as sns

# Side-by-side boxplots
both_teams_df = pd.concat((assigned_team_df, your_team_df))
plt.title('Boxplot to compare points distribution', fontsize=18) 
sns.boxplot(x='fran_id',y='pts',data=both_teams_df)
plt.show()
print("")

# Histograms
fig, ax = plt.subplots()
plt.hist(assigned_team_df['pts'], 20, alpha=0.5, label='Assigned Team')
plt.hist(your_team_df['pts'], 20, alpha=0.5, label='Your Team')
plt.title('Histogram to compare points distribution', fontsize=18) 
plt.xlabel('Points')
plt.legend(loc='upper right')
plt.show()


#  

# ## Step 6: Descriptive Statistics: Points Scored By Your Time in Home Games
# The management of your team wants you to run descriptive statistics on the points scored by your team in the games played at your team's venue in 2013-2015. Calculate descriptive statistics including the mean, median, variance, and standard deviation for points scored by your team played at Home. 

# In[6]:


print("Points Scored by Your Team in Home Games (2013 to 2015)")
print("-------------------------------------------------------")

your_team_home_df = your_team_df[your_team_df['game_location']=='H'].copy()

mean = your_team_home_df['pts'].mean()
median = your_team_home_df['pts'].median()
variance = your_team_home_df['pts'].var()
stdeviation = your_team_home_df['pts'].std()

print('Mean =', round(mean,2))
print('Median =', round(median,2))
print('Variance =', round(variance,2))
print('Standard Deviation =', round(stdeviation,2))


#  

# ## Step 7 - Descriptive Statistics - Points Scored By Your Time in Away Games
# The management also wants you to run descriptive statistics on the points scored by your team in games played at opponent's venue (Away) in 2013-2015. They want you to analyze measures of central tendency (e.g. mean, median) and measures of spread (e.g. standard deviation) in explaining if the team is doing better in Home games compared to Away games. Calculate descriptive statistics including the mean, median, variance, and standard deviation for points scored by your team played in opponent's venue (Away). 
# 

# In[7]:


print("Points Scored by Your Team in Away Games (2013 to 2015)")
print("-------------------------------------------------------")

your_team_away_df = your_team_df[your_team_df['game_location']=='A'].copy()

mean = your_team_away_df['pts'].mean()
median = your_team_away_df['pts'].median()
variance = your_team_away_df['pts'].var()
stdeviation = your_team_away_df['pts'].std()

print('Mean =', round(mean,2))
print('Median =', round(median,2))
print('Variance =', round(variance,2))
print('stdeviation =', round(stdeviation,2))


# ## Step 8: Confidence Intervals for the Average Relative Skill of All Teams in Your Team's Years
# The management wants to you to calculate a 95% confidence interval for the average relative skill of all teams in 2013-2015. You will use the variable 'elo_n' to respresent the relative skill of the teams.

# In[14]:


print("Confidence Interval for Average Relative Skill in the years 2013 to 2015")
print("------------------------------------------------------------------------------------------------------------")

# Mean relative skill of all teams from the years 2013-2015
mean = your_years_leagues_df['elo_n'].mean()

# Standard deviation of the relative skill of all teams from the years 2013-2015
stdev = your_years_leagues_df['elo_n'].std()

n = len(your_years_leagues_df)

#Confidence interval
stderr = stdev/(n ** 0.5)
conf_int_95 = st.norm.interval(0.95, mean, stderr)

print("95% confidence interval (unrounded) for Average Relative Skill (ELO) in the years 2013 to 2015 =", conf_int_95)
print("95% confidence interval (rounded) for Average Relative Skill (ELO) in the years 2013 to 2015 = (",  round(conf_int_95[0], 2),",", round(conf_int_95[1], 2),")")


print("\n")
print("Probability a team has Average Relative Skill LESS than the Average Relative Skill (ELO) of your team in the years 2013 to 2015")
print("----------------------------------------------------------------------------------------------------------------------------------------------------------")

mean_elo_your_team = your_team_df['elo_n'].mean()

choice1 = st.norm.sf(mean_elo_your_team, mean, stdev)
choice2 = st.norm.cdf(mean_elo_your_team, mean, stdev)

print("Which of the two choices is correct?")
print("Choice 1 =", round(choice1,4))
print("Choice 2 =", round(choice2,4))


# ## Step 9 - Confidence Intervals  for the Average Relative Skill of All Teams in the Assigned Team's Years
# The management also wants to you to calculate a 95% confidence interval for the average relative skill of all teams in the years 1996-1998.
# 
# The management also wants you to calculate the probability that a team had a relative skill level less than the Bulls in years 1996-1998. 
# 
# In[15]:


print('Confidence Interval for Adverage Relative Skill for the years 1996-1998')
print('----------------------------------------------------------------------------------------------------')

mean = assigned_years_league_df['elo_n'].mean()
stdev = assigned_years_league_df['elo_n'].std()
n = len(assigned_years_league_df)

stderr = stdev/(n** 0.5)
conf_int_95 = st.norm.interval(0.95, mean, stderr)

print("95% confidence interval (unrounded) for Average Relative Skill (ELO) in the years 1996 to 1998 =", conf_int_95)
print("95% confidence interval (rounded) for Average Relative Skill (ELO) in the years 1996 to 1998 = (",  round(conf_int_95[0], 2),",", round(conf_int_95[1], 2),")")

print("\n")
print("Probability a team has Average Relative Skill LESS than the Average Relative Skill (ELO) of assigned team in the years 1996 to 1998")
print("----------------------------------------------------------------------------------------------------------------------------------------------------------")

mean_elo_assigned_team = assigned_years_league_df['elo_n'].mean()

choice1 = st.norm.sf(mean_elo_assigned_team, mean, stdev)
choice2 = st.norm.cdf(mean_elo_assigned_team, mean, stdev)

print("Which of the two choices is correct?")
print("Choice 1 =", round(choice1,4))
print("Choice 2 =", round(choice2,4))


# ## End of Project One
