const mapa = document.getElementById('mapaSucursal');
const sucursalSelect = document.getElementById('sucursalSelect');

const mapas = {
  s1: "https://maps.google.com/maps?q=Plaza%20de%20Armas%20Santiago&z=15&output=embed",
  s2: "https://maps.google.com/maps?q=Las%20Condes%20Santiago&z=15&output=embed",
  s3: "https://maps.google.com/maps?q=Maipú%20Santiago&z=15&output=embed",
  s4: "https://maps.google.com/maps?q=Ñuñoa%20Santiago&z=15&output=embed",
  s5: "https://maps.google.com/maps?q=Providencia%20Santiago&z=15&output=embed",
  s6: "https://maps.google.com/maps?q=Puente%20Alto%20Santiago&z=15&output=embed",
  s7: "https://maps.google.com/maps?q=Huechuraba%20Santiago&z=15&output=embed"
};

sucursalSelect.addEventListener('change', () => {
  mapa.src = mapas[sucursalSelect.value];
});