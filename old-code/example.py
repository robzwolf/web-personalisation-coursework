# This script follows the tutorial at https://stackabuse.com/creating-a-simple-recommender-system-in-python-using-pandas/

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Forcibly display all columns when using PyCharm
# See https://stackoverflow.com/a/50947606/2176546
pd.set_option('display.max_columns', 999)
pd.set_option('display.width', 999)

ratings_data = pd.read_csv('../ml-latest-small/ratings.csv')

# head() will return the first five rows of the dataset by default
# print(ratings_data.head())

movie_names = pd.read_csv('../ml-latest-small/movies.csv')
# print(movie_names.head())

movie_data = pd.merge(ratings_data, movie_names, on='movieId')
print(movie_data.head())

# print(movie_data.groupby('title')['rating'].count().sort_values(ascending=False).head())

ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
print(ratings_mean_count.head())

sns.set_style('dark')

plt.figure(figsize=(8,6))
plt.rcParams['patch.force_edgecolor'] = True
# ratings_mean_count['rating'].hist(bins=50)
sns.jointplot(x='rating', y='rating_counts', data=ratings_mean_count, alpha=0.4)
plt.show()

user_movie_rating = movie_data.pivot_table(index='userId', columns='title', values='rating')
print(user_movie_rating.head())

forrest_gump_ratings = user_movie_rating['Forrest Gump (1994)']
print(forrest_gump_ratings.head())

movies_like_forest_gump = user_movie_rating.corrwith(forrest_gump_ratings)
corr_forrest_gump = pd.DataFrame(movies_like_forest_gump, columns=['Correlation'])
corr_forrest_gump.dropna(inplace=True)

corr_forrest_gump = corr_forrest_gump.join(ratings_mean_count['rating_counts'])
# print(corr_forrest_gump.sort_values('rating_counts', ascending=False).head(10))
print(corr_forrest_gump[corr_forrest_gump['rating_counts']>50].sort_values('Correlation', ascending=False).head())

# This will print out the five movies that are similar to Forrest Gump, based on the ratings of similar films
# by the same users.
