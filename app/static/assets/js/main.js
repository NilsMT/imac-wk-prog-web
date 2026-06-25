document.addEventListener("DOMContentLoaded", function () {
    const modalCloseButton = document.getElementById("modalCloseButton");
    modalCloseButton.addEventListener("click", function () {
        const modal = document.getElementById("modal");
        modal.querySelector(".modal-title").textContent = "";
        modal.querySelector(".modal-body").textContent = "";
        modal.querySelector(".modal-footer").innerHTML = "";
    });
});

// error alert

function showError(containerId, message) {
    const container = document.getElementById(containerId);
    if (!container) return;
    let alert = container.querySelector(".alert-feedback");
    if (alert) alert.remove();
    alert = document.createElement("div");
    alert.className =
        "alert alert-danger alert-dismissible text-white fade show alert-feedback mt-3 mb-0";
    alert.setAttribute("role", "alert");
    alert.innerHTML = `
    <span class="alert-icon align-middle">
      <span class="material-symbols-rounded text-md">error</span>
    </span>
    <span class="alert-text">${message}</span>
    <button type="button" class="btn-close" data-bs-dismiss="alert" style="padding-top: 1rem; padding-bottom: 1rem;" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>`;
    container.appendChild(alert);
}

function hideError(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const alert = container.querySelector(".alert-feedback");
    if (alert) alert.remove();
}

// success alert

function showSuccess(formId, message) {
    let successDiv = document.getElementById(`${formId}-success`);
    if (!successDiv) {
        successDiv = document.createElement("div");
        successDiv.id = `${formId}-success`;
        successDiv.className = "alert alert-success mt-3";
        document.getElementById(formId).appendChild(successDiv);
    }
    successDiv.textContent = message;
    successDiv.style.display = "block";
}

function hideSuccess(formId) {
    const successDiv = document.getElementById(`${formId}-success`);
    if (successDiv) successDiv.style.display = "none";
}

// input status update
function updateFieldStatus(input, groupId) {
    const group = document.getElementById(groupId);
    const inputGroup = group.querySelector(".input-group-outline");
    if (input.value.trim() === "") {
        inputGroup.classList.remove("is-valid", "is-invalid");
    }
}

// validators
function verifyEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function verifyPromo(promo) {
    const currentYear = new Date().getFullYear();
    const promoNum = parseInt(promo, 10);
    return !isNaN(promoNum) && promoNum >= 2010 && promoNum <= currentYear + 3;
}
