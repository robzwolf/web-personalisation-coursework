# Web Technology Coursework

## Requirements
- Python 3.7.4
- numpy 1.17.4 (and scipy)
- pandas 0.25.3
- Flask 1.1.1

This application is likely to work with slightly different versions of the above requirements,  however the above
requirements are the only guaranteed combination of dependencies.


## Quick Start
```
cd code/
pip3 install numpy
pip3 install pandas
pip3 install Flask
python3 server.py
```

Server will now be running on http://localhost:5000


## Summary of Work
This application utilises SVD matrix factorisation to recommend books in Python. Much of the core logic borrows heavily
from https://beckernick.github.io/matrix-factorization-recommender/, retrieved 21/12/2019.


### The Dataset

Creating the dataset was particularly challenging. This application uses a modified version of the 
[goodbooks-10k](http://fastml.com/goodbooks-10k-a-new-dataset-for-book-recommendations/) dataset of books, which
comprises 10,000 books and roughly 180,000 ratings from users. This is reduced from the original dataset of roughly
3 million ratings, for speed. 

There are two files in the `dataset/` directory:
- `ratings-small.csv`, which contains `user_id`, `book_id` and `rating` columns
- `books_metadata.csv`, which contains `book_id`, `title` and `genres` columns

The `genres` column contains a list of genres (chosen by users) for each book, separated by a vertical pipe `|`.

 
### Recommending Books to Users

We use SVD matrix factorisation to recommend books to users. For this application, you can enter a user ID into the
search field (of the website) and it will issue an AJAX request to get recommendations for that user.

The server will receive the request and run the matrix factorisation algorithm accordingly to get a list of
recommended books for that user, by looking up that user's ratings of other books and finding books that users with
similar ratings histories also liked. 
