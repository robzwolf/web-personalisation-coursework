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
ratings_mean_count['rating_counts'].hist(bins=50)
plt.show()
