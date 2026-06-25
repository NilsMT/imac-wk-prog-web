function loadComments(eventId) {
    const commentsContainer = document.getElementById(
        `comments-container-${eventId}`,
    );

    fetch(`/api/v1/comments/${eventId}`)
        .then((res) => res.json())
        .then((comments) => {
            if (comments.length === 0) {
                commentsContainer.innerHTML = `<p class="text-muted">Aucun message pour cet événement.</p>`;
                return;
            }
            const fullName = (c) =>
                `${c.firstname} ${c.name}` || c.pseudo || "Utilisateur inconnu";
            commentsContainer.innerHTML = comments
                .map(
                    (comment) => `
        <div class="mb-3 p-2 bg-light rounded">
          <div class="d-flex justify-content-between align-items-center gap-2 mb-1">
            <strong>${fullName(comment)}</strong>
            <small class="text-muted">${new Date(comment.datetime).toLocaleString("fr-FR")}</small>
          </div>
          <p class="mb-0">${comment.message}</p>
        </div>
      `,
                )
                .join("");
            commentsContainer.scrollTop = commentsContainer.scrollHeight;
        })
        .catch((error) => {
            console.error("Erreur lors du chargement des messages:", error);
            commentsContainer.innerHTML = `<div class="alert alert-danger text-white" role="alert">Impossible de charger les messages.</div>`;
        });
}

function sendComment(eventId) {
    const messageInput = document.getElementById(`message-input-${eventId}`);
    const message = messageInput.value.trim();
    if (!message) return;

    fetch(`/api/v1/comments/${eventId}`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `message=${encodeURIComponent(message)}`,
    })
        .then((res) => res.json().then((data) => ({ ok: res.ok, data })))
        .then(({ ok, data }) => {
            if (ok) {
                messageInput.value = "";
                loadComments(eventId);
            } else {
                showError(`comments-container-${eventId}`, data.message);
            }
        })
        .catch((error) => {
            showError(
                `comments-container-${eventId}`,
                "Une erreur est survenue. Veuillez réessayer.",
            );
        });
}

function toggleParticipation(eventId, isParticipating) {
    fetch(`/api/v1/participations/${eventId}`, {
        method: isParticipating ? "POST" : "DELETE",
        headers: { "Content-Type": "application/json" },
    })
        .then((res) => res.json().then((data) => ({ ok: res.ok, data })))
        .then(({ ok, data }) => {
            if (ok) {
                loadEventDetails(eventId);
            } else {
                document.getElementById(
                    `participationToggle-${eventId}`,
                ).checked = !isParticipating;
                showError(`eventCard-${eventId}`, data.message);
            }
        })
        .catch(() => {
            document.getElementById(`participationToggle-${eventId}`).checked =
                !isParticipating;
            showError(
                `eventCard-${eventId}`,
                "Une erreur est survenue. Veuillez réessayer.",
            );
        });
}

function loadEventDetails(eventId) {
    const modalEvent = document.getElementById("modal");
    const modalTitle = modalEvent.querySelector(".modal-title");
    const modalBody = modalEvent.querySelector(".modal-body");
    const modalFooter = modalEvent.querySelector(".modal-footer");

    modalFooter.style.display = "none";
    modalTitle.textContent = "Détails de l'événement";
    modalEvent.classList.add("modal-xl");

    Promise.all([
        fetch(`/api/v1/events/${eventId}`).then((res) => res.json()),
        fetch(`/api/v1/participations/${eventId}`).then((res) => res.json()),
    ])
        .then(([event, participationResponse]) => {
            const isParticipating = participationResponse.participe === 1;

            modalBody.innerHTML = `
        <div class="row g-4">
          <div class="col-md-7">
            <div class="card shadow-lg h-100" id="eventCard-${eventId}">
              <img src="${event.image || window.location.origin + "/static/uploads/default.jpg"}" class="card-img-top" alt="Image de l'événement" style="height: 180px; object-fit: cover" />
              <div class="card-body p-4">
                <h3 class="card-title text-dark mb-3">${event.name}</h3>
                <div class="d-flex justify-content-between mb-3 text-muted align-items-center">
                  <div class="d-flex align-items-center">
                    <i class="material-symbols-rounded me-2 text-dark">calendar_month</i>
                    ${
                        event.end_date.substring(0, 10) ===
                        event.start_date.substring(0, 10)
                            ? `<span>${event.start_date.substring(8, 10)}/${event.start_date.substring(5, 7)}/${event.start_date.substring(0, 4)}</span>
                         <span class="text-muted ps-2">(${event.start_date.substring(11, 16).replace(":", "h")} → ${event.end_date.substring(11, 16).replace(":", "h")})</span>`
                            : `<span>${event.start_date.substring(8, 10)}/${event.start_date.substring(5, 7)}/${event.start_date.substring(0, 4)} (${event.start_date.substring(11, 16).replace(":", "h")})</span>
                         <span class="text-muted px-2">→</span>
                         <span class="text-muted">${event.end_date.substring(8, 10)}/${event.end_date.substring(5, 7)}/${event.end_date.substring(0, 4)} (${event.end_date.substring(11, 16).replace(":", "h")})</span>`
                    }
                  </div>
                  <div class="d-flex align-items-center">
                    <i class="material-symbols-rounded me-2 text-dark">location_on</i>
                    <span>${event.location}</span>
                  </div>
                </div>
                <div class="d-flex align-items-center mb-3">
                  <i class="material-symbols-rounded me-2 text-dark">group</i>
                  <span id="participantsCount">${event.nb_participants} participant${event.nb_participants !== 1 ? "s" : ""}</span>
                </div>
                <p class="card-text text-muted mb-4">${event.description || "Aucune description"}</p>
                ${
                    event.attributes && event.attributes.length > 0
                        ? `<div class="mb-3">${event.attributes
                              .map(
                                  (attr) => `
                      <div class="d-flex align-items-center">
                        <span class="me-2 text-dark text-bold">${attr.name} :</span>
                        <span>${attr.value}</span>
                      </div>`,
                              )
                              .join("")}
                     </div>`
                        : ""
                }
                <div class="d-flex align-items-center mt-3">
                  <label class="switch m-0">
                    <input type="checkbox" id="participationToggle-${eventId}" ${isParticipating ? "checked" : ""} onchange="toggleParticipation(${eventId}, this.checked)" />
                    <span class="slider round"></span>
                  </label>
                  <span class="ms-3" id="participationLabel-${eventId}">${isParticipating ? "Je participe !" : "Je ne participe pas"}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-5">
            <div class="card h-100">
              <div class="card-header bg-gradient-dark">
                <h5 class="mb-0 text-white">Messages</h5>
              </div>
              <div id="comments-container-${eventId}" class="card-body p-3" style="max-height: 400px; overflow-y: auto;">
                <p class="text-muted">Chargement des messages...</p>
              </div>
              <div class="card-footer p-3">
                <div class="input-group input-group-outline">
                  <input type="text" id="message-input-${eventId}" class="form-control" placeholder="Écrivez un message..." onkeypress="if(event.key === 'Enter') sendComment(${eventId})" />
                  <button class="btn btn-info m-0" onclick="sendComment(${eventId})">
                    <i class="material-symbols-rounded">send</i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;

            loadComments(eventId);
        })
        .catch((error) => {
            console.error("Erreur:", error);
            modalBody.innerHTML = `
        <div class="alert alert-danger alert-dismissible text-white fade show" role="alert">
          <span class="alert-icon align-middle"><span class="material-symbols-rounded text-md">error</span></span>
          <span class="alert-text">Impossible de charger les détails de l'événement.</span>
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        </div>`;
        });
}

document.addEventListener("DOMContentLoaded", function () {
    const modalEvent = document.getElementById("modal");

    document.querySelectorAll(".viewEventButton").forEach((button) => {
        button.addEventListener("click", function () {
            loadEventDetails(this.getAttribute("data-event-id"));
        });
    });

    modalEvent.addEventListener("hidden.bs.modal", function () {
        modalEvent.querySelector(".modal-body").innerHTML = "";
        modalEvent.querySelector(".modal-title").textContent = "";
        modalEvent.querySelector(".modal-footer").style.display = "block";
        modalEvent.classList.remove("modal-xl");
    });
});
