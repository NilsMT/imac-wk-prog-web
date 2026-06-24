document.addEventListener("DOMContentLoaded", function () {
  const modalCloseButton = document.getElementById("modalCloseButton");
  modalCloseButton.addEventListener("click", function () {
    const modal = document.getElementById("modal");
    const modalTitle = modal.querySelector(".modal-title");
    const modalBody = modal.querySelector(".modal-body");
    const modalFooter = modal.querySelector(".modal-footer");
  });
});
