function verifyEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function verifyPromo(promo) {
    const currentYear = new Date().getFullYear();
    const promoNum = parseInt(promo, 10);
    return !isNaN(promoNum) && promoNum >= 2010 && promoNum <= currentYear + 3;
}

function validateForm() {
    const firstname = document.getElementById("firstname").value.trim();
    const name = document.getElementById("name").value.trim();
    const pseudo = document.getElementById("pseudo").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const promo = document.getElementById("promo").value.trim();
    return firstname && name && pseudo && email && verifyEmail(email) && password && promo && verifyPromo(promo);
}

function setFieldValid(groupId, isValid) {
    const group = document.getElementById(groupId);
    const inputGroup = group.querySelector(".input-group-outline") || group;
    inputGroup.classList.toggle("is-valid", isValid);
    inputGroup.classList.toggle("is-invalid", !isValid && inputGroup.querySelector("input").value.trim() !== "");
}

document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");
    const submitButton = document.getElementById("submitButton");
    submitButton.disabled = true;

    const fields = [
        { id: "firstname", groupId: "firstnameGroup", validate: v => v.trim() !== "" },
        { id: "name",      groupId: "nameGroup",      validate: v => v.trim() !== "" },
        { id: "pseudo",    groupId: "pseudoGroup",    validate: v => v.trim() !== "" },
        { id: "email",     groupId: "emailGroup",     validate: v => verifyEmail(v) },
        { id: "password",  groupId: "passwordGroup",  validate: v => v.trim() !== "" },
        { id: "promo",     groupId: "promoGroup",     validate: v => verifyPromo(v) },
    ];

    fields.forEach(({ id, groupId, validate }) => {
        document.getElementById(id).addEventListener("input", function () {
            setFieldValid(groupId, validate(this.value));
            submitButton.disabled = !validateForm();
        });
    });

    registerForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        if (!validateForm()) return;

        hideError("registerForm");

        const formData = new FormData(registerForm);
        const response = await fetch("/api/v1/users", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = "/";
        } else {
            showError("registerForm", result.message || "Erreur lors de l'inscription.");
        }
    });
});
