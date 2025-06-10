document.getElementById('formContacto').addEventListener('submit', function (e) {
    e.preventDefault();

    const datos = {
      nombre: this.querySelector('input[placeholder="Nombre"]').value,
      email: this.querySelector('input[placeholder="Email"]').value,
      asunto: this.querySelector('input[placeholder="Asunto"]').value,
      mensaje: this.querySelector('textarea').value,
    };

    fetch('/api/contacto/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos),
    })
    .then(response => response.json())
    .then(data => {
      alert(data.mensaje);
    })
    .catch(error => {
      alert('Ocurrió un error al enviar el mensaje.');
    });
  });