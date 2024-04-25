document.addEventListener("DOMContentLoaded", function () {
  $(function () {
    const alertPlaceholder = document.getElementById("liveAlertPlaceholder");
    const appendAlert = (message, type) => {
      const wrapper = document.createElement("div");
      wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible" role="alert">`,
        `   <div>${message}</div>`,
        "</div>",
      ].join("");

      alertPlaceholder.append(wrapper);
      // Remove the alert after 3 seconds
      setTimeout(() => {
        wrapper.remove();
      }, 3000);
    };

    const alertTrigger = document.getElementById("liveAlertBtn");
    if (alertTrigger) {
      alertTrigger.addEventListener("click", () => {
        appendAlert(
          "Identifiant du groupe copié dans le presse-papiers!",
          "success"
        );
      });
    }
  });

  // Activer le datepicker pour le champ de saisie de la date
  $(function () {
    $("#date").datepicker({ dateFormat: "yy-mm-dd" });
  });

  // Activer les time pickers pour les champs de saisie des heures de début et de fin
  $(function () {
    $("#heure-debut, #heure-fin").timepicker({
      timeFormat: "H:i",
      dropdown: false,
    });
  });

  var creneauForm = document.getElementById("creneau-form");
  if (creneauForm) {
    creneauForm.addEventListener("submit", submitForm);
  }

  function submitForm(event) {
    event.preventDefault(); // Empêche le comportement par défaut du formulaire

    // Récupérer les données du formulaire
    var formData = $("#creneau-form").serialize();

    // Envoyer les données du formulaire au serveur de manière asynchrone
    $.ajax({
      type: "POST",
      url: "/sauvegarder-creneau",
      data: formData,
      success: function (response) {
        // Faire quelque chose en cas de succès, par exemple afficher un message de confirmation
        alert(response);
      },
      error: function (xhr, status, error) {
        // Gérer les erreurs en cas d'échec de la requête
        console.error(error);
      },
    });
  }

  document
    .getElementById("liveAlertBtn")
    .addEventListener("click", function () {
      // Sélectionne l'élément contenant la valeur à copier
      var elementToCopy = document.getElementById("group-id");

      // Sélectionne la valeur à copier
      var textToCopy = elementToCopy.value;

      // Crée un élément de texte temporaire pour copier la valeur
      var tempInput = document.createElement("input");
      tempInput.setAttribute("value", textToCopy);
      document.body.appendChild(tempInput);

      // Sélectionne et copie la valeur
      tempInput.select();
      document.execCommand("copy");

      // Supprime l'élément temporaire
      document.body.removeChild(tempInput);
    });
});
