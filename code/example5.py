# Sort books metadata CSV by ratings_count
import pandas as pd
from time import process_time

# Forcibly display all columns when using PyCharm
# See https://stackoverflow.com/a/50947606/2176546
pd.set_option('display.max_columns', 999)
pd.set_option('display.width', 999)

books_list = pd.read_csv('books_metadata.csv')
books_df = pd.DataFrame(books_list, columns=['book_id', 'title', 'genres'])

ratings_list = pd.read_csv('../goodbooks-10k/ratings.csv')
ratings_df = pd.DataFrame(ratings_list, columns=['user_id', 'book_id', 'rating'])

print(books_df.head())
print(ratings_df.head())

book_data = pd.merge(ratings_df, books_df, on='book_id')
# print(book_data.groupby('title')['rating'].count().sort_values(ascending=False).head())

ratings_mean_count = pd.DataFrame(book_data.groupby('title')['rating'].mean())
ratings_mean_count['rating_counts'] = pd.DataFrame(book_data.groupby('title')['rating'].count())

print(ratings_mean_count.sort_values(ascending=False, by='rating_counts').head(50))

# user_book_rating = book_data.pivot_table(index='user_id', columns='title', values='rating')
# print(user_book_rating.head())
