// Fonction pour vérifier l'email
function verifyEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Fonction pour vérifier la promotion
function verifyPromo(promo) {
  const currentYear = new Date().getFullYear();
  const minYear = 2010;
  const maxYear = currentYear + 3;
  const promoNum = parseInt(promo, 10);
  return !isNaN(promoNum) && promoNum >= minYear && promoNum <= maxYear;
}

// Fonction pour vérifier si le formulaire est valide
function validateForm() {
  const firstname = document.getElementById("firstname").value.trim();
  const name = document.getElementById("name").value.trim();
  const pseudo = document.getElementById("pseudo").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const promo = document.getElementById("promo").value.trim();

  return (
    firstname !== "" &&
    name !== "" &&
    pseudo !== "" &&
    email !== "" &&
    verifyEmail(email) &&
    password !== "" &&
    promo !== "" &&
    verifyPromo(promo)
  );
}

// Écouteurs pour la validation en temps réel
document.addEventListener("DOMContentLoaded", function () {
  const registerForm = document.getElementById("registerForm");
  const firstnameInput = document.getElementById("firstname");
  const nameInput = document.getElementById("name");
  const pseudoInput = document.getElementById("pseudo");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const promoInput = document.getElementById("promo");
  const submitButton = document.getElementById("submitButton");
  submitButton.disabled = true;

  // Fonction pour mettre à jour l'état d'un champ (avec input-group-outline)
  function updateFieldStatus(input, groupId) {
    const group = document.getElementById(groupId);
    const inputGroup = group.querySelector(".input-group-outline");

    if (input.value.trim() === "") {
      inputGroup.classList.remove("is-valid", "is-invalid");
    }
  }

  // Écouteurs pour chaque champ
  firstnameInput.addEventListener("input", function () {
    const isValid = this.value.trim() !== "";
    updateFieldStatus(this, "firstnameGroup");
    if (isValid) {
      document
        .getElementById("firstnameGroup")
        .querySelector(".input-group-outline")
        .classList.add("is-valid");
    } else {
      document
        .getElementById("firstnameGroup")
        .querySelector(".input-group-outline")
        .classList.remove("is-valid");
    }
    submitButton.disabled = !validateForm();
  });

  nameInput.addEventListener("input", function () {
    const isValid = this.value.trim() !== "";
    updateFieldStatus(this, "nameGroup");
    if (isValid) {
      document
        .getElementById("nameGroup")
        .querySelector(".input-group-outline")
        .classList.add("is-valid");
    } else {
      document
        .getElementById("nameGroup")
        .querySelector(".input-group-outline")
        .classList.remove("is-valid");
    }
    submitButton.disabled = !validateForm();
  });

  pseudoInput.addEventListener("input", function () {
    const isValid = this.value.trim() !== "";
    updateFieldStatus(this, "pseudoGroup");
    if (isValid) {
      document
        .getElementById("pseudoGroup")
        .querySelector(".input-group-outline")
        .classList.add("is-valid");
    } else {
      document
        .getElementById("pseudoGroup")
        .querySelector(".input-group-outline")
        .classList.remove("is-valid");
    }
    submitButton.disabled = !validateForm();
  });

  emailInput.addEventListener("input", function () {
    const isValid = this.value.trim() !== "" && verifyEmail(this.value);
    updateFieldStatus(this, "emailGroup");
    if (isValid) {
      document
        .getElementById("emailGroup")
        .querySelector(".input-group-outline")
        .classList.add("is-valid");
    } else {
      document
        .getElementById("emailGroup")
        .querySelector(".input-group-outline")
        .classList.remove("is-valid");
    }
    submitButton.disabled = !validateForm();
  });

  passwordInput.addEventListener("input", function () {
    const isValid = this.value.trim() !== "";
    updateFieldStatus(this, "passwordGroup");
    if (isValid) {
      document
        .getElementById("passwordGroup")
        .querySelector(".input-group-outline")
        .classList.add("is-valid");
    } else {
      document
        .getElementById("passwordGroup")
        .querySelector(".input-group-outline")
        .classList.remove("is-valid");
    }
    submitButton.disabled = !validateForm();
  });

  promoInput.addEventListener("input", function () {
    const isValid = verifyPromo(this.value);
    updateFieldStatus(this, "promoGroup");
    if (isValid) {
      document
        .getElementById("promoGroup")
        .querySelector(".input-group-outline")
        .classList.add("is-valid");
    } else {
      document
        .getElementById("promoGroup")
        .querySelector(".input-group-outline")
        .classList.remove("is-valid");
    }
    submitButton.disabled = !validateForm();
  });

  // Soumission du formulaire
  registerForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const isFormValid = validateForm();

    if (isFormValid) {
      const formData = new FormData(registerForm);

      const response = await fetch("/user/register", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      console.log(result);

      if (response.ok) {
        window.location.href = "/dashboard";
      }
    }
  });
});
