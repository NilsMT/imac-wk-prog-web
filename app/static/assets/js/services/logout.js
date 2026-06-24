document.addEventListener("DOMContentLoaded", function () {
    const logoutModalButton = document.getElementById("logoutModalButton");
    const modal = document.getElementById("modal");
    const modalTitle = modal.querySelector(".modal-title");
    const modalBody = modal.querySelector(".modal-body");
    const modalFooter = modal.querySelector(".modal-footer");
    logoutModalButton.addEventListener("click", function () {
        modalTitle.textContent = "Confirmation de déconnexion";
        modalBody.textContent = "Êtes-vous sûr de vouloir vous déconnecter ?";
        modalFooter.innerHTML = `
      <button type="button" class="btn btn-secondary" id="modalCancelButton" data-bs-dismiss="modal">Annuler</button>
      <a id="logoutButton" class="btn btn-danger">Se déconnecter</a>
    `;

        const modalCancelButton = document.getElementById("modalCancelButton");
        modalCancelButton.addEventListener("click", function () {
            modalTitle.textContent = "";
            modalBody.textContent = "";
            modalFooter.innerHTML = "";
        });

        const logoutButton = document.getElementById("logoutButton");
        logoutButton.addEventListener("click", async function () {
            try {
                const response = await fetch("/api/v1/session", {
                    method: "DELETE",
                });

                if (response.ok) {
                    window.location.href = "/login";
                }
            } catch (error) {
                console.error("Erreur lors de la déconnexion :", error);
            }
        });
    });
});
