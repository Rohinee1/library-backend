let allBooks = [];
let editId = null;

/* LOAD BOOKS */
function loadBooks() {
    fetch(`${BASE_URL}/books/`)
    .then(res => res.json())
    .then(data => {
        allBooks = data;
        renderBooks(data);
    });
}

/* RENDER */
function renderBooks(data) {
    const container = document.getElementById("books");
    container.innerHTML = "";

    if (!data.length) {
        container.innerHTML = "<p>No books found</p>";
        return;
    }

    data.forEach(b => {
        container.innerHTML += `
        <div class="col-md-3">
            <div class="card p-3 mb-3">
                <h5>${b.title}</h5>
                <p>${b.author}</p>

                <button onclick="openEdit('${b._id}')" class="btn btn-warning btn-sm">Edit</button>
                <button onclick="deleteBook('${b._id}')" class="btn btn-danger btn-sm">Delete</button>
            </div>
        </div>
        `;
    });
}

/* SEARCH */
function searchBooks(q) {
    const filtered = allBooks.filter(b =>
        b.title.toLowerCase().includes(q.toLowerCase())
    );
    renderBooks(filtered);
}

/* OPEN MODAL */
function openAdd() {
    editId = null;
    document.getElementById("form").reset();
    new bootstrap.Modal(document.getElementById("bookModal")).show();
}

/* OPEN EDIT */
function openEdit(id) {
    editId = id;
    const b = allBooks.find(x => x._id === id);

    document.getElementById("title").value = b.title;
    document.getElementById("author").value = b.author;
    document.getElementById("isbn").value = b.isbn;
    document.getElementById("category").value = b.category;
    document.getElementById("quantity").value = b.quantity;

    new bootstrap.Modal(document.getElementById("bookModal")).show();
}

/* SAVE (ADD + EDIT) */
function saveBook() {

    const token = localStorage.getItem("token");

    const book = {
        title: title.value,
        author: author.value,
        isbn: isbn.value,
        category: category.value,
        quantity: quantity.value
    };

    let url = `${BASE_URL}/books/add`;
    let method = "POST";

    if (editId) {
        url = `${BASE_URL}/books/${editId}`;
        method = "PUT";
    }

    fetch(url, {
        method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify(book)
    })
    .then(res => res.json())
    .then(data => {
        showAlert(data.message || data.error, "success");
        loadBooks();
    });
}

/* DELETE */
function deleteBook(id) {
    const token = localStorage.getItem("token");

    fetch(`${BASE_URL}/books/${id}`, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + token }
    })
    .then(res => res.json())
    .then(data => {
        showAlert(data.message || data.error, "danger");
        loadBooks();
    });
}

/* ALERT */
function showAlert(msg, type) {
    const alertBox = document.getElementById("alert");
    alertBox.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
    setTimeout(() => alertBox.innerHTML = "", 3000);
}

window.onload = loadBooks;