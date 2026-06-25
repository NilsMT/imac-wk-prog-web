function validateForm() {
    const firstname = document.getElementById("firstname").value.trim();
    const name = document.getElementById("name").value.trim();
    const pseudo = document.getElementById("pseudo").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const promo = document.getElementById("promo").value.trim();
    return (
        firstname &&
        name &&
        pseudo &&
        email &&
        verifyEmail(email) &&
        password &&
        promo &&
        verifyPromo(promo)
    );
}

document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");
    const submitButton = document.getElementById("submitButton");
    submitButton.disabled = true;

    const fields = [
        {
            id: "firstname",
            groupId: "firstnameGroup",
            validate: (v) => v.trim() !== "",
        },
        { id: "name", groupId: "nameGroup", validate: (v) => v.trim() !== "" },
        {
            id: "pseudo",
            groupId: "pseudoGroup",
            validate: (v) => v.trim() !== "",
        },
        { id: "email", groupId: "emailGroup", validate: (v) => verifyEmail(v) },
        {
            id: "password",
            groupId: "passwordGroup",
            validate: (v) => v.trim() !== "",
        },
        { id: "promo", groupId: "promoGroup", validate: (v) => verifyPromo(v) },
    ];

    fields.forEach(({ id, groupId, validate }) => {
        document.getElementById(id).addEventListener("input", function () {
            updateFieldStatus(this, groupId);
            const inputGroup = document
                .getElementById(groupId)
                .querySelector(".input-group-outline");
            if (validate(this.value)) {
                inputGroup.classList.add("is-valid");
            } else {
                inputGroup.classList.remove("is-valid");
            }
            submitButton.disabled = !validateForm();
        });
    });

    registerForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        if (!validateForm()) return;

        hideError("registerForm");

        const response = await fetch("/api/v1/users", {
            method: "POST",
            body: new FormData(registerForm),
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = "/";
        } else {
            showError(
                "registerForm",
                result.message || "Erreur lors de l'inscription.",
            );
        }
    });
});
