import pandas as pd
from time import process_time

# Forcibly display all columns when using PyCharm
# See https://stackoverflow.com/a/50947606/2176546
pd.set_option('display.max_columns', 999)
pd.set_option('display.width', 999)

ratings_list = pd.read_csv('../goodbooks-10k/ratings.csv')
books_list = pd.read_csv('../goodbooks-10k/books.csv')
tags_list = pd.read_csv('../goodbooks-10k/tags.csv')
tags_dict = pd.read_csv('../goodbooks-10k/tags.csv', squeeze=True, index_col=0).to_dict()
book_tags_list = pd.read_csv('../goodbooks-10k/book_tags.csv')

# print(ratings_list.head())
# print(books_list.head())
# print(tags_list.head())
# print(book_tags_list.head(30))

ratings_df = pd.DataFrame(ratings_list, columns=['user_id', 'book_id', 'rating'])
# print(ratings_df.head())

books_df = pd.DataFrame(books_list, columns=['goodreads_book_id', 'work_id', 'title'])
# print(books_df.head())

tags_df = pd.DataFrame(tags_list, columns=['tag_id', 'tag_name'])
# print(tags_df.head())

# tags_dict = pd.Series.from_csv('../goodbooks-10k/tags.csv', header=0).to_dict()
# print(tags_list)
print(tags_dict)
# print(tags_list.to_dict())

book_tags_df = pd.DataFrame(book_tags_list, columns=['goodreads_book_id', 'tag_id', 'count'])
books_df['genres'] = ''
print(books_df.head())


def get_genre_from_tag_id(tag_id):
    return tags_dict[tag_id]


# Loop through each book_tag_mapping
counter = 0
counter_2 = 0
total = book_tags_df.shape[0]
print('Starting now...')
start_time = process_time()
for book_tag_mapping in book_tags_df.itertuples():
    tag_id = getattr(book_tag_mapping, 'tag_id')
    current_goodreads_book_id = getattr(book_tag_mapping, 'goodreads_book_id')

    # Get the genre associated with that tag ID
    genre = get_genre_from_tag_id(tag_id)

    # Update the genres column for that goodreads_book_id
    current_genres = books_df.loc[(books_df['goodreads_book_id'] == current_goodreads_book_id, 'genres')].values[0]
    # new_genres = '{0}{1}|'.format(current_genres, genre)# current_genres + genre + '|'
    new_genres = f'{current_genres}{genre}|'
    # print('current_genres ' + current_genres)
    # print(type(current_genres))
    # print('genre ' + genre)
    # print('new_genres ' + new_genres)

    try:
        books_df.loc[books_df['goodreads_book_id'] == current_goodreads_book_id, 'genres'] = new_genres
    except Exception:
        print('Error with:')
        print(book_tag_mapping)
        print(genre)
        continue

    counter += 1
    counter_2 += 1

    if counter % 10000 == 0:
        print(str(counter / 10000) + str('% complete'))
        # counter = 0

    # if counter > 20000:
    #     break

print('Mapped ' + str(counter_2) + ' mappings.')
elapsed_time = process_time() - start_time
print('Took {} seconds.'.format(elapsed_time))
print(books_df.head(50))

books_df.to_csv(f'books_df-{process_time()}.csv')


# tags_df = pd.DataFrame(tags_list, columns)
