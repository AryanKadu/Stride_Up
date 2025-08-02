const features = [
    { title: "Expert Trainers", text: "Work with professional trainers to achieve your fitness goals." },
    { title: "Personalized Workouts", text: "Customized workout plans tailored just for you." },
    { title: "Track Your Progress", text: "Monitor your improvement with detailed progress tracking." }
];
let currentFeature = 0;

document.getElementById("prevFeature").addEventListener("click", function() {
    currentFeature = (currentFeature - 1 + features.length) % features.length;
    updateFeature();
});

document.getElementById("nextFeature").addEventListener("click", function() {
    currentFeature = (currentFeature + 1) % features.length;
    updateFeature();
});

function updateFeature() {
    document.getElementById("featureTitle").textContent = features[currentFeature].title;
    document.getElementById("featureText").textContent = features[currentFeature].text;
}


document.addEventListener("DOMContentLoaded", function () {
initCounters();
initTrainersCarousel();
});

// Hero Carousel Functions
document.addEventListener("DOMContentLoaded", () => {
initCarousel();
});
function initCarousel() {
let currentIndex = 0;
const slides = document.querySelectorAll(".slide");
const totalSlides = slides.length;

function changeSlide(direction) {
slides[currentIndex].classList.remove("active");
currentIndex = (currentIndex + direction + totalSlides) % totalSlides;
slides[currentIndex].classList.add("active");
document.querySelector(".carousel-images").style.transform = `translateX(-${currentIndex * 100}%)`;
}

// Auto-slide function
function autoSlide() {
changeSlide(1);
}
setInterval(autoSlide, 3000); // Auto slide every 3 seconds
}



//  Counter Animation

function initCounters() {
function animateCounter(id, start, end, duration) {
    let range = end - start;
    let current = start;
    let stepTime = Math.abs(Math.floor(duration / range));
    let element = document.getElementById(id);

    if (!element) return;

    let timer = setInterval(() => {
        current += 1;
        element.textContent = current;
        if (current >= end) clearInterval(timer);
    }, stepTime);
}

// Initialize counters (change values if needed)
animateCounter("users-count", 0, 5000, 2000);
animateCounter("trainers-count", 0, 20, 1500);
animateCounter("sessions-count", 0, 5000, 2000);
animateCounter("years-count", 0, 10, 1000);
}


//Trainers Carousel

function initTrainersCarousel() {
const carousel = document.querySelector(".trainers-carousel");
const prevBtn = document.querySelector(".prev-btn");
const nextBtn = document.querySelector(".next-btn");

if (!carousel || !prevBtn || !nextBtn) return;

const trainerElement = document.querySelector(".trainer");
const trainerWidth = trainerElement ? trainerElement.offsetWidth + 20 : 200;

nextBtn.addEventListener("click", () => {
    carousel.scrollBy({ left: trainerWidth * 2, behavior: "smooth" });
});

prevBtn.addEventListener("click", () => {
    carousel.scrollBy({ left: -trainerWidth * 2, behavior: "smooth" });
});

// Mobile swipe support
let touchStartX = 0;
let touchEndX = 0;

carousel.addEventListener(
    "touchstart",
    (e) => (touchStartX = e.changedTouches[0].screenX),
    { passive: true }
);

carousel.addEventListener(
    "touchend",
    (e) => {
        touchEndX = e.changedTouches[0].screenX;
        if (touchEndX < touchStartX) {
            carousel.scrollBy({ left: trainerWidth * 2, behavior: "smooth" });
        } else if (touchEndX > touchStartX) {
            carousel.scrollBy({ left: -trainerWidth * 2, behavior: "smooth" });
        }
    },
    { passive: true }
);
}