document.addEventListener("DOMContentLoaded", function () {
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

// Fonction pour charger les groupes après la création d'un nouveau groupe
function loadUserGroups(listeGroupe) {
  // Générer le HTML des groupes à partir des données passées en argument
  var userGroupsHTML = '<h2 class="display-5">Groupes de l\'utilisateur</h2>';

  // Parcourir les groupes et construire le HTML pour chaque groupe
  for (var i = 0; i < listeGroupe.length; i++) {
    var group = listeGroupe[i];
    userGroupsHTML += '<a href="/groupe-details?id=' + group.id + '" class="d-block mb-2">';
    userGroupsHTML += '<button class="btn btn-outline-light">' + group.name + '</button>';
    userGroupsHTML += '</a>';
  }

  // Mettre à jour la partie de la page qui affiche les groupes avec le HTML généré
  $('#user-groups').html(userGroupsHTML);
}


var newGroupeForm = document.getElementById("new-group-form");
  if (newGroupeForm) {
    newGroupeForm.addEventListener("submit", submitNewGroupForm);
  }

function submitNewGroupForm(event) {
  event.preventDefault(); // Empêche le comportement par défaut du formulaire
  
  // Récupérer les données du formulaire
  var formData = $('#new-group-form').serialize();
  
  // Envoyer les données du formulaire au serveur de manière asynchrone
  $.ajax({
    type: 'POST',
    url: '/creer-groupe',
    data: formData,
    success: function(response) {
      // Faire quelque chose en cas de succès, par exemple afficher un message de confirmation
      alert(response.message);
      loadUserGroups(response.listeGroupe)
      },
    error: function(xhr, status, error) {
      // Gérer les erreurs en cas d'échec de la requête
      console.error(error);
    }
  });
}

var joinForm = document.getElementById("join-form");
  if (joinForm) {
    joinForm.addEventListener("submit", submitJoinGroup);
  }

function submitJoinGroup(event) {
  event.preventDefault(); // Empêche le comportement par défaut du formulaire
  
  // Récupérer les données du formulaire
  var formData = $('#join-form').serialize();
  
  // Envoyer les données du formulaire au serveur de manière asynchrone
  $.ajax({
    type: 'POST',
    url: '/rejoindre-groupe',
    data: formData,
    success: function(response) {
      // Faire quelque chose en cas de succès, par exemple afficher un message de confirmation
      alert(response.message);
      loadUserGroups(response.listeGroupe)
      },
    error: function(xhr, status, error) {
      // Gérer les erreurs en cas d'échec de la requête
      console.error(error);
    }
  });
}

var creneauForm = document.getElementById("creneau-form");
  if (creneauForm) {
    creneauForm.addEventListener("submit", submitForm);
  }

function submitForm(event) {
  event.preventDefault(); // Empêche le comportement par défaut du formulaire

  // Récupérer les données du formulaire
  var formData = $('#creneau-form').serialize();

  // Envoyer les données du formulaire au serveur de manière asynchrone
  $.ajax({
    type: 'POST',
    url: '/sauvegarder-creneau-user',
    data: formData,
    success: function(response) {
      // Faire quelque chose en cas de succès, par exemple afficher un message de confirmation
      alert(response);
      },
    error: function(xhr, status, error) {
      // Gérer les erreurs en cas d'échec de la requête
      console.error(error);
    }
  });
}

  document
    .getElementById("toggleButton")
    .addEventListener("click", function () {
      var contentDiv = document.getElementById("userid");
      contentDiv.classList.toggle("d-none");
    });

  document
    .getElementById("liveAlertBtn")
    .addEventListener("click", function () {
      // Sélectionne l'élément contenant la valeur à copier
      var elementToCopy = document.getElementById("user-id");

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
          "Identifiant de l'utilisateur copié dans le presse-papiers!",
          "success"
        );
      });
    }
  });
});
