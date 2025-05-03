const isMobile = window.innerWidth <= 991;

const swiperConfig = {
  slidesPerView: 'auto',
  centeredSlides: true,
  spaceBetween: 16,
  loop: true,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  breakpoints: {
    768: {
      centeredSlides: false,
      slidesPerView: 2,
      spaceBetween: 24,
    },
    1024: {
      centeredSlides: false,
      slidesPerView: 3,
      spaceBetween: 30,
    },
  },
};

if (isMobile) {
  swiperConfig.autoplay = {
    delay: 1,
    disableOnInteraction: false,
    pauseOnMouseEnter: true,
  };
  swiperConfig.speed = 4000;
}

const swiper = new Swiper('.swiper', swiperConfig);



const swiperContainer = document.querySelector('.swiper');
swiperContainer.addEventListener('mouseenter', () => {
  swiper.autoplay.stop();
});

swiperContainer.addEventListener('mouseleave', () => {
  swiper.autoplay.start();
});

  const navbarLinks = document.querySelectorAll('#navbarModal a');

  navbarLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();

      const target = this.getAttribute('href');
      const modal = bootstrap.Modal.getInstance(document.getElementById('navbarModal'));

      if (modal) {
        modal.hide();

        setTimeout(() => {
          const section = document.querySelector(target);
          if (section) {
            section.scrollIntoView({ behavior: 'smooth' });
          }
        }, 300);
      }
    });
  });


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
      if (window.location.pathname === "/" && link && modalElement) {
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
  
  
  