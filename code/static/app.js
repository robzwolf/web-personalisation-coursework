const loadingBox = document.querySelector('#loading');
const resultsBox = document.querySelector('#results');

function getRecommendations() {
    loadingBox.classList.remove('hidden');
    resultsBox.classList.add('hidden');

    const userID = document.querySelector('#user_id').value;

    fetch(`/api/${userID}`)
        .then(response => response.json())
        .then(json => displayBooksList(json.predictions));


}

function displayBooksList(books) {
    const ul = document.querySelector('.books-predictions');
    ul.innerHTML = '';

    books.forEach(book => {
        const li = `<li>${book.title}</li>`;
        ul.innerHTML += li;
    });

    loadingBox.classList.add('hidden');
    resultsBox.classList.remove('hidden');
}
