document.addEventListener("DOMContentLoaded", function () {
    const modalElement = document.getElementById("navbarModal");
  
    const enlaces = [
      "link-inicio-modal",
      "link-quienes-modal",
      "link-productos-modal",
      "link-contacto-modal"
    ];
  
    enlaces.forEach(id => {
      const link = document.getElementById(id);
      if (link && modalElement) {
        link.addEventListener("click", function (e) {
          e.preventDefault();
  
          const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
          modal.hide();
  
          setTimeout(() => {
            window.location.href = link.dataset.url;
          }, 300);
        });
      }
    });
  });
  