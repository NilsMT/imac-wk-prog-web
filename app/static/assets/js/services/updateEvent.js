async function editEvent(eventId) {
  const modalEvent = document.getElementById("modal");
  const modalTitle = modalEvent.querySelector(".modal-title");
  const modalBody = modalEvent.querySelector(".modal-body");
  const modalFooter = modalEvent.querySelector(".modal-footer");

  modalTitle.textContent = "Modifier l'évévement";
  modalFooter.style.display = "flex";
  modalFooter.innerHTML = `
      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
      <button type="button" class="btn btn-info" id="confirmEditBtn">Confirmer</button>
  `;
  modalEvent.classList.add("modal-xl");

  try {
    const response = await fetch(`/api/v1/events/${eventId}`);
    if (!response.ok) {
      throw new Error("Erreur lors de la récupération des données de l'événement.");
    }
    const event = await response.json();

    const formatDateForInput = (dateString) => {
      if (!dateString) return "";
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");
      return `${year}-${month}-${day}T${hours}:${minutes}`;
    };

    modalBody.innerHTML = `
      <form id="editEventForm" enctype="multipart/form-data">
        <!-- Nom de l'événement -->
        <div class="imput-group input-group-lg input-group-outline my-3">
          <label for="editEventName" class="form-label">
            Nom de l'événement
            <span class="text-danger">*</span>
          </label>
          <input 
            type="text" 
            class="form-control 
            form-control-lg" 
            id="editEventName" 
            name="name" 
            value="${event.name}" 
            required
          />
        </div>

        <!-- Dates -->
        <div class="row mb-3">
          <div class="col-md-6">
              <div class="input-group input-group-lg input-group-static my-3">
                <label for="editEventStartDate">
                  Date de début
                  <span class="text-danger">*</span>
                </label>
                <input
                  type="datetime-local"
                  class="form-control form-control-lg"
                  id="editEventStartDate"
                  name="start_date"
                  value="${formatDateForInput(event.start_date)}"
                  required
                />
              </div>
          </div>
          <div class="col-md-6">
              <div class="input-group input-group-lg input-group-static my-3">
                <label for="editEventEndDate">
                  Date de fin
                  <span class="text-danger">*</span>
                </label>
                <input
                  type="datetime-local"
                  class="form-control form-control-lg"
                  id="editEventEndDate"
                  name="end_date"
                  value="${formatDateForInput(event.end_date)}"
                  required
                />
              </div>
          </div>
        </div>

        <!-- Lieu de l'événement -->
        <div class="imput-group input-group-lg input-group-outline my-3">
          <label for="editEventLocation" class="form-label">
            Lieu
            <span class="text-danger">*</span>
          </label>
          <input 
            type="text" 
            class="form-control 
            form-control-lg" 
            id="editEventLocation" 
            name="location" 
            value="${event.location}" 
            required
          />
        </div>

        <!-- Description -->
          <div class="input-group input-group-lg input-group-outline my-3">
            <textarea
              class="form-control"
              id="editEvenDescription"
              name="description"
              rows="3"
              placeholder="Description de l'événement"
            >${event.description || ""}</textarea>
          </div>
          
        <!-- Image -->
        <div class="row mb-3">
          <div class="col-md-6">
            <div class="input-group input-group-lg input-group-static my-3">
              <label for="image">Image de l'événement</label>
              <input
                type="file"
                class="form-control form-control-lg"
                id="image"
                name="image"
                accept="image/png, image/jpg, image/jpeg, image/gif"
              />
              <div class="form-text text-muted">
                Formats autorisés : PNG, JPG, JPEG, GIF (max 16 Mo).
              </div>
            </div>
          </div>
          <div class="col-md-6 d-flex column align-items-center">
            <h6 class="mb-0">Image actuelle :</h6>
            <img
              src="${event.image || '/static/uploads/default.jpg'}"
              alt="Image de l'événement"
              class="img-fluid ms-3"
              style="max-height: 100px; max-width: 100%; object-fit: cover; border-radius: 4px;"
            />
          </div>
        </div>

        <!-- Attributs -->
          <div class="mt-3">
            <label class="form-label">Attributs</label>
            <div id="editAttributesContainer" class="mt-2">
              <!-- Les attributs seront ajoutés ici dynamiquement -->
            </div>
            <button
              type="button"
              id="editAddAttributeBtn"
              class="btn btn-outline-secondary mt-2 d-flex align-items-center"
            >
              <i class="btn-inner--icon material-symbols-rounded me-1">add</i>
              <span class="btn-inner--text">Ajouter un attribut</span>
            </button>
          </div>
      </form>
    `;
    
    const attributesContainer = document.getElementById(
      "editAttributesContainer",
    );
    const addAttributeBtn = document.getElementById("editAddAttributeBtn");
    let editAttributeCounter = 0;

    if (event.attributes && event.attributes.length > 0) {
      event.attributes.forEach((attribute) => {
        editAttributeCounter++;
        const attributeId = `editAttribute${editAttributeCounter}`;
        const attributeGroup = document.createElement("div");
        attributeGroup.className = "row mb-2 g-2 align-items-center justify-content-between";
        attributeGroup.id = attributeId;

        attributeGroup.innerHTML = `
          <div class="col-md-5">
            <div class="input-group input-group-lg input-group-outline">
              <input
                type="text"
                class="form-control form-control-lg"
                name="attributeName${editAttributeCounter}"
                value="${attribute.name}"
                required
              />
            </div>
          </div>
          <div class="col-md-5">
            <div class="input-group input-group-lg input-group-outline">
              <input
                type="text"
                class="form-control form-control-lg"
                name="attributeValue${editAttributeCounter}"
                value="${attribute.value}"
                required
              />
            </div>
          </div>
          <div class="col-md-2 d-flex align-items-center">
            <button
              type="button"
              class="btn btn-danger w-100 remove-attribute mb-0 d-flex align-items-center justify-content-center"
              data-attribute-id="${attributeId}"
            >
              <i class="material-symbols-rounded text-md py-1">delete</i>
            </button>
          </div>
        `;

        attributesContainer.appendChild(attributeGroup);
        attributeGroup
        .querySelector(".remove-attribute")
        .addEventListener("click", function () {
          document.getElementById(this.getAttribute("data-attribute-id")).remove();
        });
      });
    }

    addAttributeBtn.addEventListener("click", function () {
      editAttributeCounter++;
      const attributeId = `editAttribute${editAttributeCounter}`;
      const attributeGroup = document.createElement("div");
      attributeGroup.className = "row mb-2 g-2 align-items-center justify-content-between";
      attributeGroup.id = attributeId;

      attributeGroup.innerHTML = `
        <div class="col-md-5">
          <div class="input-group input-group-lg input-group-outline">
            <input
              type="text"
              class="form-control form-control-lg"
              name="attributeName${editAttributeCounter}"
              placeholder="Nom (ex: Musique)"
              required
            />
          </div>
        </div>
        <div class="col-md-5">
          <div class="input-group input-group-lg input-group-outline">
            <input
              type="text"
              class="form-control form-control-lg"
              name="attributeValue${editAttributeCounter}"
              placeholder="Valeur (ex: Rock)"
              required
            />
          </div>
        </div>
        <div class="col-md-2 d-flex align-items-center">
          <button
            type="button"
            class="btn btn-danger w-100 remove-attribute mb-0 d-flex align-items-center justify-content-center"
            data-attribute-id="${attributeId}"
          >
            <i class="material-symbols-rounded text-md py-1">delete</i>
          </button>
        </div>
      `;

      attributesContainer.appendChild(attributeGroup);
      attributeGroup
      .querySelector(".remove-attribute")
      .addEventListener("click", function () {
        document.getElementById(this.getAttribute("data-attribute-id")).remove();
      });
    });

    document.getElementById("confirmEditBtn").addEventListener("click", async function () {
      this.disabled = true;
      const form = document.getElementById("editEventForm");
      const formData = new FormData(form);

      const attributes = [];
      const attributeInputs = form.querySelectorAll(
        "[name^='attributeName']",
      );

      attributeInputs.forEach((input, index) => {
        const name = input.value;
        const valueInput = form.querySelector(
          `[name='attributeValue${index + 1}']`,
        );
        const value = valueInput ? valueInput.value : "";
        if (name && value) {
          attributes.push({ type:"TEXT", name: name, value: value });
        }
      });

      console.log("Attributs collectés :", attributes);

      const eventData = {
        name: formData.get("name"),
        start_date: new Date(formData.get("start_date")).toISOString(),
        end_date: new Date(formData.get("end_date")).toISOString(),
        location: formData.get("location"),
        description: formData.get("description"),
        attributes: attributes,
      };

      const finalFormData = new FormData();
      finalFormData.append("eventData", JSON.stringify(eventData));
      if (formData.get("image") && formData.get("image").size > 0) {
        finalFormData.append("image", formData.get("image"));
      }

      try {
        const response = await fetch(`/api/v1/events/${eventId}`, {
          method: "PUT",
          body: finalFormData,
        });

        const result = await response.json();
        if (response.ok) {
          bootstrap.Modal.getInstance(modalEvent).hide();
          window.location.reload();
        } else {
          alert(result.message || "Erreur lors de la mise à jour de l'événement.");
        }
      } catch (error) {
        console.error("Erreur lors de la mise à jour de l'événement:", error);
      } finally {
        this.disabled = false;
      }
    });
  } catch (error) {
    console.error("Erreur lors de la récupération des données de l'événement:", error);
    modalBody.innerHTML = `
      <div class="alert alert-danger">
        Impossible de charger les détails de l'événement.
      </div>
    `;
  }
}

// Evenement sur les boutons
document.addEventListener("DOMContentLoaded", function () {
  const modalEvent = document.getElementById("modal");
  document.querySelectorAll(".editEventButton").forEach((button) => {
    button.addEventListener("click", function () {
      const eventId = this.getAttribute("data-event-id");
      editEvent(eventId);
    });
  });

  modalEvent.addEventListener("hidden.bs.modal", function () {
    const modalBody = modalEvent.querySelector(".modal-body");
    const modalTitle = modalEvent.querySelector(".modal-title");
    const modalFooter = modalEvent.querySelector(".modal-footer");
    modalBody.innerHTML = "";
    modalTitle.textContent = "";
    modalFooter.style.display = "block";
    modalEvent.classList.remove("modal-xl");
  });
});