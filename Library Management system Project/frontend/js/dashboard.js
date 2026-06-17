const API = "http://127.0.0.1:5000/api/books";

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "index.html";
        return;
    }

    loadBooks();
});

// Logout
function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

// Add Book
document.getElementById("bookForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");

    const book = {
        title: document.getElementById("title").value,
        author: document.getElementById("author").value,
        isbn: document.getElementById("isbn").value,
        category: document.getElementById("category").value,
        quantity: document.getElementById("quantity").value
    };

    const res = await fetch(`${API}/add`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`  // 🔥 REQUIRED
        },
        body: JSON.stringify(book)
    });

    const data = await res.json();
    alert(data.message || data.error);

    loadBooks();
});

// Load Books
async function loadBooks() {
    const res = await fetch(`${API}/`);
    const books = await res.json();

    const list = document.getElementById("bookList");
    list.innerHTML = "";

    books.forEach(book => {
        const li = document.createElement("li");

        li.innerHTML = `
            <b>${book.title}</b> by ${book.author}
            (Available: ${book.available})
            <button onclick="deleteBook('${book._id}')">Delete</button>
        `;

        list.appendChild(li);
    });
}

// Delete Book
async function deleteBook(id) {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API}/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await res.json();
    alert(data.message || data.error);

    loadBooks();
}