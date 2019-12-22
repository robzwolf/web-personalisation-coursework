# Follows https://beckernick.github.io/matrix-factorization-recommender/

import pandas as pd
import numpy as np
from time import process_time
from scipy.sparse.linalg import svds

start_time = process_time()
print('Starting...')

# Forcibly display all columns when using PyCharm
# See https://stackoverflow.com/a/50947606/2176546
pd.set_option('display.max_columns', 999)
pd.set_option('display.width', 999)

ratings_list = pd.read_csv('../master-dataset/ratings-small.csv')
books_list = pd.read_csv('../master-dataset/books_metadata.csv')

ratings_df = pd.DataFrame(ratings_list, columns=['user_id', 'book_id', 'rating'], dtype=int)
books_df = pd.DataFrame(books_list, columns=['book_id', 'title', 'genres'])
books_df['book_id'] = books_df['book_id'].apply(pd.to_numeric)

print(ratings_df.head())
print(books_df.head())

R_df = ratings_df.pivot(index='user_id', columns='book_id', values='rating').fillna(0)
# print(R_df.head())

R = R_df.values
user_ratings_mean = np.mean(R, axis=1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)

U, sigma, Vt = svds(R_demeaned, k=50)
sigma = np.diag(sigma)

all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns=R_df.columns)


def recommend_books(predictions_df, user_id, books_df, original_ratings_df, num_recommendations=5):
    # Get and sort the user's predictions
    user_row_number = user_id - 1  # user_id starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)

    # Get the user's data and merge in the book information
    user_data = original_ratings_df[original_ratings_df.user_id == (user_id)]
    user_full = (user_data.merge(books_df, how='left', left_on='book_id', right_on='book_id')
                 .sort_values(['rating'], ascending=False))

    print('User {0} has already rated {1} books.'.format(user_id, user_full.shape[0]))
    print('Recommending the highest {0} predicted rating books not already rated.'.format(num_recommendations))

    # Recommend the highest predicted rating books that the user hasn't seen yet.
    recommendations = (books_df[~books_df['book_id'].isin(user_full['book_id'])]
    .merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left', left_on='book_id', right_on='book_id')
                       .rename(columns={user_row_number: 'predictions'})
                       .sort_values('predictions', ascending=False)
                       .iloc[:num_recommendations, :-1])

    return user_full, recommendations


user_id = 89
already_rated, predictions = recommend_books(preds_df, user_id, books_df, ratings_df, 10)
print(already_rated.head(10))
print(predictions)

print(f'Process took {str(process_time() - start_time)} seconds.')
