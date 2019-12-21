# This script follows the tutorial at https://beckernick.github.io/matrix-factorization-recommender/

import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

# Forcibly display all columns when using PyCharm
# See https://stackoverflow.com/a/50947606/2176546
pd.set_option('display.max_columns', 999)
pd.set_option('display.width', 999)

ratings_list = pd.read_csv('../ml-latest-small/ratings.csv')
movies_list = pd.read_csv('../ml-latest-small/movies.csv')

ratings_df = pd.DataFrame(ratings_list, columns=['userId', 'movieId', 'rating', 'timestamp'], dtype=int)
movies_df = pd.DataFrame(movies_list, columns=['movieId', 'title', 'genres'])
movies_df['movieId'] = movies_df['movieId'].apply(pd.to_numeric)

print(movies_df.head())
print(ratings_df.head())

R_df = ratings_df.pivot(index='userId', columns='movieId', values='rating').fillna(0)
print(R_df.head())

R = R_df.as_matrix()
user_ratings_mean = np.mean(R, axis=1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)

U, sigma, Vt = svds(R_demeaned, k=50)
sigma = np.diag(sigma)

all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns=R_df.columns)


def recommend_movies(predictions_df, userId, movies_df, original_ratings_df, num_recommendations=5):
    # Get and sort the user's predictions
    user_row_number = userId - 1  # userId starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)

    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.userId == (userId)]
    user_full = (user_data.merge(movies_df, how='left', left_on='movieId', right_on='movieId')
                 .sort_values(['rating'], ascending=False)
                 )

    print('User {0} has already rated {1} movies'.format(userId, user_full.shape[0]))
    print('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))

    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (movies_df[~movies_df['movieId'].isin(user_full['movieId'])]
                           .merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left', left_on='movieId',
                                  right_on='movieId')
                           .rename(columns={user_row_number: 'predictions'})
                           .sort_values('predictions', ascending=False)
                           .iloc[:num_recommendations, :-1]
                           )

    return user_full, recommendations


already_rated, predictions = recommend_movies(preds_df, 45, movies_df, ratings_df, 10)
print('already_rated (first 10):')
print(already_rated.head(10))
print()

print('predictions (first 10):')
print(predictions.head(10))
