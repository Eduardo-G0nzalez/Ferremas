function toggleForms(target) {
    const loginForm = document.getElementById("login-form");
    const registroForm = document.getElementById("registro-form");
  
    if (!loginForm || !registroForm) return;
  
    loginForm.classList.remove("active");
    registroForm.classList.remove("active");
  
    if (target === "login") {
      loginForm.classList.add("active");
    } else {
      registroForm.classList.add("active");
    }
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    const hash = window.location.hash;
  
    // Previene el scroll automático del navegador
    if (hash === "#registro-form" || hash === "#login-form") {
      setTimeout(() => {
        window.scrollTo(0, 0); // vuelve arriba
        toggleForms(hash === "#registro-form" ? "registro" : "login");
        history.replaceState(null, null, window.location.pathname); // limpia el hash
      }, 0);
    }
  });
  