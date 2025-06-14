document.addEventListener("DOMContentLoaded", function () {
    const mainImg = document.getElementById('mainImage');
    const miniaturas = document.querySelectorAll('.miniatura');
  
    miniaturas.forEach(img => {
      img.addEventListener('click', function () {
        mainImg.src = this.dataset.full;
  
        // Quitar clase activa a todas
        miniaturas.forEach(i => i.classList.remove('active-thumbnail'));
  
        // Activar la que se hizo click
        this.classList.add('active-thumbnail');
      });
    });
  
    // Activar la primera miniatura por defecto solo si ninguna ya tiene active
    if (miniaturas.length > 0 && !document.querySelector('.miniatura.active-thumbnail')) {
      miniaturas[0].classList.add('active-thumbnail');
    }
  });

  // Esperar a que el DOM cargue
  document.addEventListener('DOMContentLoaded', function () {
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.forEach(function (toastEl) {
      const toast = new bootstrap.Toast(toastEl, {
        delay: 2000,
        autohide: true
      });
      toast.show();
    });
  });
  