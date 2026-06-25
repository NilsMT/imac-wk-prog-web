function validateProfileForm() {
    const name = document.getElementById("name").value.trim();
    const firstname = document.getElementById("firstname").value.trim();
    const promo = document.getElementById("promo").value.trim();
    const email = document.getElementById("email").value.trim();
    const pseudo = document.getElementById("pseudo").value.trim();
    return (
        name && firstname && verifyPromo(promo) && verifyEmail(email) && pseudo
    );
}

function validatePasswordForm() {
    const currentPassword = document
        .getElementById("currentPassword")
        .value.trim();
    const newPassword = document.getElementById("newPassword").value.trim();
    const confirmPassword = document
        .getElementById("confirmPassword")
        .value.trim();
    return currentPassword && newPassword && newPassword === confirmPassword;
}

function updateFieldStatus(input) {
    const inputGroup = input.closest(".input-group-outline");
    if (!inputGroup) return;
    if (input.value.trim() === "") {
        inputGroup.classList.remove("is-valid", "is-invalid");
    }
}

async function updateInfos() {
    const form = document.getElementById("profileForm");
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        const input = form.querySelector(`[name=\"${key}\"]`);
        if (input && input.hasAttribute("readonly")) return;
        if (value !== "") data[key] = value;
    });

    hideError("profileForm");

    const response = await fetch("/api/v1/users", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    const result = await response.json();
    if (response.ok) {
        showSuccess("profileForm", result.message);
    } else {
        showError("profileForm", result.message, [
            "firstname",
            "name",
            "promo",
        ]);
    }
}

async function updatePassword() {
    const form = document.getElementById("passwordForm");
    const formData = new FormData(form);
    const currentPassword = formData.get("currentPassword");
    const newPassword = formData.get("newPassword");
    const confirmPassword = formData.get("confirmPassword");

    if (newPassword !== confirmPassword) {
        showError("passwordForm", "Les mots de passe ne correspondent pas", [
            "newPassword",
            "confirmPassword",
        ]);
        return;
    }

    hideError("passwordForm");

    const response = await fetch("/api/v1/users/password", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ currentPassword, newPassword }),
    });

    const result = await response.json();
    if (response.ok) {
        showSuccess("passwordForm", result.message);
        form.reset();
        document.getElementById("submitPasswordBtn").disabled = true;
    } else {
        const fields = result.message.includes("actuel")
            ? ["currentPassword"]
            : ["newPassword", "confirmPassword"];
        showError("passwordForm", result.message, fields);
    }
}

document.addEventListener("DOMContentLoaded", async function () {
    const profileSubmitBtn = document.getElementById("submitBtn");
    const passwordSubmitBtn = document.getElementById("submitPasswordBtn");
    if (profileSubmitBtn) profileSubmitBtn.disabled = true;
    if (passwordSubmitBtn) passwordSubmitBtn.disabled = true;

    const profileFields = [
        { id: "firstname", validate: (v) => v.trim() !== "" },
        { id: "name", validate: (v) => v.trim() !== "" },
        { id: "promo", validate: (v) => verifyPromo(v) },
        { id: "email", validate: (v) => verifyEmail(v) },
        { id: "pseudo", validate: (v) => v.trim() !== "" },
    ];

    const passwordFields = [
        { id: "currentPassword", validate: (v) => v.trim() !== "" },
        {
            id: "newPassword",
            validate: (v) => v.trim() !== "" && v.length >= 8,
        },
        {
            id: "confirmPassword",
            validate: (v) => v.trim() !== "" && v.length >= 8,
        },
    ];

    const allFields = [...profileFields, ...passwordFields];

    allFields.forEach(({ id, validate }) => {
        const input = document.getElementById(id);
        if (!input) return;
        input.addEventListener("input", function () {
            updateFieldStatus(this);
            const inputGroup = this.closest(".input-group-outline");
            if (validate(this.value)) {
                inputGroup.classList.add("is-valid");
            } else {
                inputGroup.classList.remove("is-valid");
            }

            if (profileFields.some((f) => f.id === id) && profileSubmitBtn) {
                profileSubmitBtn.disabled = !validateProfileForm();
            }
            if (passwordFields.some((f) => f.id === id) && passwordSubmitBtn) {
                passwordSubmitBtn.disabled = !validatePasswordForm();
            }
        });
    });

    const response = await fetch("/api/v1/users/me");
    const user = response.ok ? await response.json() : {};

    if (user.email) document.getElementById("email").value = user.email;
    if (user.pseudo) document.getElementById("pseudo").value = user.pseudo;
    if (user.name) document.getElementById("name").value = user.name;
    if (user.firstname)
        document.getElementById("firstname").value = user.firstname;
    if (user.promo) document.getElementById("promo").value = user.promo;

    ["firstname", "name", "promo", "email", "pseudo"].forEach((id) => {
        const input = document.getElementById(id);
        if (input && input.value) {
            const inputGroup = input.closest(".input-group-outline");
            if (inputGroup) inputGroup.classList.add("is-filled");
            input.dispatchEvent(new Event("input", { bubbles: true }));
        }
    });

    document
        .getElementById("profileForm")
        .addEventListener("submit", function (e) {
            e.preventDefault();
            if (!validateProfileForm()) return;
            updateInfos();
        });

    document
        .getElementById("passwordForm")
        .addEventListener("submit", function (e) {
            e.preventDefault();
            if (!validatePasswordForm()) return;
            updatePassword();
        });
});
