async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const message = document.getElementById("message");

    if (!email || !password) {
        message.innerHTML =
            '<div class="alert alert-danger">Please fill all fields.</div>';
        return;
    }

    try {

        const response = await fetch(`${BASE_URL}/api/users/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {

            localStorage.setItem("token", data.token);

            message.innerHTML =
                '<div class="alert alert-success">Login successful!</div>';

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1000);

        } else {

            message.innerHTML =
                `<div class="alert alert-danger">${data.message}</div>`;
        }

    } catch (error) {

        message.innerHTML =
            '<div class="alert alert-danger">Backend server not running.</div>';

        console.error(error);
    }
}