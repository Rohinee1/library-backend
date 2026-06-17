function showPage(pageId) {
    document.querySelectorAll(".page-section")
        .forEach(p => p.classList.remove("active"));

    document.getElementById(pageId).classList.add("active");

    if (pageId === "catalog") {
        loadBooks();
    }
}