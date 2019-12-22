const loadingBox = document.querySelector('#loading');
const resultsBox = document.querySelector('#results');

function getRecommendations() {
    const userIdElement = document.querySelector('#user_id');
    if (!userIdElement.checkValidity()) {
        return;
    }

    loadingBox.classList.remove('hidden');
    resultsBox.classList.add('hidden');

    const userID = userIdElement.value;

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
