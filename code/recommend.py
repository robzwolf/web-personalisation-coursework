# Follows https://stackabuse.com/creating-a-simple-recommender-system-in-python-using-pandas/

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from time import process_time

print('Starting script...')
start_time = process_time()

sns.set_style('dark')

# Forcibly display all columns when using PyCharm
# See https://stackoverflow.com/a/50947606/2176546
pd.set_option('display.max_columns', 999)
pd.set_option('display.width', 999)

ratings_data = pd.read_csv('../master-dataset/ratings.csv')
# print(ratings_data.head())

book_names = pd.read_csv('../master-dataset/books_metadata.csv')
# print(book_names.head())

book_data = pd.merge(ratings_data, book_names, on='book_id')
# print(book_data.groupby('title')['rating'].count().sort_values(ascending=False).head())

ratings_mean_count = pd.DataFrame(book_data.groupby('title')['rating'].mean())
ratings_mean_count['rating_counts'] = pd.DataFrame(book_data.groupby('title')['rating'].count())
# print(ratings_mean_count.head())

# plt.figure(figsize=(8,6))
# plt.rcParams['patch.force_edgecolor'] = True
# # ratings_mean_count['rating'].hist(bins=50)
# sns.jointplot(x='rating', y='rating_counts', data=ratings_mean_count, alpha=0.4)
# plt.show()

user_book_rating = book_data.pivot_table(index='user_id', columns='title', values='rating')
# print(user_book_rating.head())

chosen_book = 'The Hunger Games (The Hunger Games, #1)'
chosen_book_ratings = user_book_rating[chosen_book]
# print(chosen_book_ratings.head())

books_like_chosen_book = user_book_rating.corrwith(chosen_book_ratings)
corr_chosen_book = pd.DataFrame(books_like_chosen_book, columns=['Correlation'])
corr_chosen_book.dropna(inplace=True)
# print(corr_chosen_book.head())
corr_chosen_book = corr_chosen_book.join(ratings_mean_count['rating_counts'])
similar_books = corr_chosen_book[corr_chosen_book['rating_counts']>1000].sort_values('Correlation', ascending=False)
print(similar_books.head(10))

print(f'Finished in {process_time() - start_time} seconds.')
