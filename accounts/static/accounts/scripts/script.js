// Carousel functionality
const slides = document.querySelectorAll('.hero__slide');
let currentSlide = 0;

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.style.display = i === index ? 'block' : 'none';
  });
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide(currentSlide);
}

setInterval(nextSlide, 5000);

// Newsletter submission
const newsletterForm = document.querySelector('.newsletter__form');

if (newsletterForm) {
  newsletterForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const input = this.querySelector('.newsletter__input');
    if (input.value.trim() !== '') {
      alert('Thanks for subscribing with: ' + input.value);
      input.value = '';
    } else {
      alert('Please enter a valid email.');
    }
  });
}
