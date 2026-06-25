document.addEventListener("DOMContentLoaded", function () {
    const modalCloseButton = document.getElementById("modalCloseButton");
    modalCloseButton.addEventListener("click", function () {
        const modal = document.getElementById("modal");
        modal.querySelector(".modal-title").textContent = "";
        modal.querySelector(".modal-body").textContent = "";
        modal.querySelector(".modal-footer").innerHTML = "";
    });
});

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
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
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
