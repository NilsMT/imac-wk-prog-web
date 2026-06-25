function verifyEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateForm() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    return email.trim() !== "" && verifyEmail(email) && password.trim() !== "";
}

document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const submitButton = loginForm.querySelector("button[type='submit']");
    submitButton.disabled = true;

    emailInput.addEventListener("input", function () {
        const isValid = verifyEmail(this.value);
        const emailGroup = document.getElementById("emailGroup");
        emailGroup.classList.toggle("is-invalid", !isValid);
        emailGroup.classList.toggle("is-valid", isValid);
        submitButton.disabled = !validateForm();
    });

    passwordInput.addEventListener("input", function () {
        const isValid = this.value.trim() !== "";
        const passwordGroup = document.getElementById("passwordGroup");
        passwordGroup.classList.toggle("is-invalid", !isValid);
        passwordGroup.classList.toggle("is-valid", isValid);
        submitButton.disabled = !validateForm();
    });

    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        if (!validateForm()) return;

        hideError("loginForm");

        const response = await fetch("/api/v1/session", {
            method: "POST",
            body: new FormData(loginForm),
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = "/";
        } else {
            showError("loginForm", result.message || "Erreur lors de la connexion.");
        }
    });
});
