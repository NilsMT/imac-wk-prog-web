document.addEventListener("DOMContentLoaded", function () {
  const attributesContainer = document.getElementById("attributesContainer");
  const addAttributeBtn = document.getElementById("addAttributeBtn");
  const eventForm = document.getElementById("eventForm");
  const submitBtn = document.getElementById("submitBtn");
  const submitText = document.getElementById("submitText");

  let attributeCounter = 0;

  addAttributeBtn.addEventListener("click", function () {
    attributeCounter++;
    const attributeId = `attribute-${attributeCounter}`;

    const attributeGroup = document.createElement("div");
    attributeGroup.className =
      "row mb-2 g-2 align-items-center justify-content-between";
    attributeGroup.id = attributeId;

    attributeGroup.innerHTML = `
      <div class="col-md-5">
        <div class="input-group input-group-lg input-group-outline">
          <input
            type="text"
            class="form-control form-control-lg"
            name="attribute_name_${attributeCounter}"
            placeholder="Nom (ex: Musique)"
            required
          >
        </div>
      </div>
      <div class="col-md-5">
        <div class="input-group input-group-lg input-group-outline">
          <input
            type="text"
            class="form-control form-control-lg"
            name="attribute_value_${attributeCounter}"
            placeholder="Valeur (ex: Jazz)"
            required
          >
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
        document.getElementById(this.dataset.attributeId).remove();
      });
  });

  eventForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    submitBtn.disabled = true;

    const formData = new FormData(eventForm);

    const attributes = [];
    const attributeInputs = eventForm.querySelectorAll(
      "[name^='attribute_name_']",
    );
    attributeInputs.forEach((input, index) => {
      const name = input.value;
      const valueInput = eventForm.querySelector(
        `[name="attribute_value_${index + 1}"]`,
      );
      const value = valueInput ? valueInput.value : "";
      const type = "TEXT";
      if (name && value) {
        attributes.push({ type: type, name: name, value: value });
      }
    });

    const eventData = {
      name: formData.get("name"),
      start_date: new Date(formData.get("start_date")),
      end_date: new Date(formData.get("end_date")),
      location: formData.get("location"),
      description: formData.get("description"),
      attributes: attributes,
    };

    const finalFormData = new FormData();
    finalFormData.append("eventData", JSON.stringify(eventData));
    if (formData.get("image")) {
      finalFormData.append("image", formData.get("image"));
    }

    try {
      const response = await fetch("/api/v1/events", {
        method: "POST",
        body: finalFormData,
      });

      const result = await response.json();

      if (response.ok) {
        window.location.href = "/myEvents";
      } else {
        alert(result.message || "Erreur lors de la création de l'événement.");
      }
    } catch (error) {
      alert("Erreur de connexion au serveur : " + error.message);
    } finally {
      submitBtn.disabled = false;
    }
  });
});
