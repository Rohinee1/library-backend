// Make function global so button can call it
window.login = async function () {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const msg = document.getElementById("message");

    try {
        const res = await fetch("http://127.0.0.1:5000/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (res.ok) {
            // Save token
            localStorage.setItem("token", data.access_token);

            msg.innerHTML = "<span style='color:green'>Login successful</span>";

            // Redirect
            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 800);

        } else {
            msg.innerHTML = `<span style="color:red">${data.error || "Login failed"}</span>`;
        }

    } catch (err) {
        console.error("Error:", err);
        msg.innerHTML = "<span style='color:red'>Server not reachable</span>";
    }
    
    function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}
};