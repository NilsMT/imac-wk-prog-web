function verifyEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateForm() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const isEmailValid = email.trim() !== "" && verifyEmail(email);
    const isPasswordValid = password.trim() !== "";

    return isEmailValid && isPasswordValid;
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("login.js loaded");
    const loginForm = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const submitButton = loginForm.querySelector("button[type='submit']");
    submitButton.disabled = true;

    emailInput.addEventListener("input", async function () {
        const email = this.value;
        const isValid = await verifyEmail(email);
        const emailGroup = document.getElementById("emailGroup");

        if (isValid) {
            emailGroup.classList.remove("is-invalid");
            emailGroup.classList.add("is-valid");
        } else {
            emailGroup.classList.remove("is-valid");
            emailGroup.classList.add("is-invalid");
        }
    });

    passwordInput.addEventListener("input", function () {
        const isValid = this.value.trim() !== "";
        const passwordGroup = document.getElementById("passwordGroup");
        if (isValid) {
            passwordGroup.classList.remove("is-invalid");
            passwordGroup.classList.add("is-valid");
        } else {
            passwordGroup.classList.remove("is-valid");
            passwordGroup.classList.add("is-invalid");
        }
    });

    emailInput.addEventListener("input", function () {
        submitButton.disabled = !validateForm();
    });

    passwordInput.addEventListener("input", function () {
        submitButton.disabled = !validateForm();
    });

    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const isFormValid = validateForm();

        if (isFormValid) {
            const formData = new FormData(loginForm);

            const response = await fetch("/api/v1/session", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            console.log(result);

            if (response.ok) {
                window.location.href = "/";
            }
        }
    });
});
