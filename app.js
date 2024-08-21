$(document).ready(function(){

    // Function to handle scrolling behavior
    $(window).scroll(function(){

        // Add sticky class to navbar when scrolling down
        if(this.scrollY > 200){
            $('.navbar').addClass("sticky");
        } else {
            $('.navbar').removeClass("sticky");
        }

        // Show/hide scroll-up button
        if(this.scrollY > 500){
            $('.scroll-up-btn').addClass("show");
        } else {
            $('.scroll-up-btn').removeClass("show");
        }   
    });

    // Initialize typed.js for dynamic typing effect
    var typed1 = new Typed(".typing-1",{
        strings: ["Unbiased Summaries", "Authentic ", "Concise"],
        typeSpeed: 100,
        backSpeed: 60,
        loop: true
    });

    // var typed2 = new Typed(".typing-2",{
    //     strings: ["Insightful", "Dynamic", "Innovative"],
    //     typeSpeed: 100,
    //     backSpeed: 60,
    //     loop: true
    // });

    // Functionality for scroll-up button
    $('.scroll-up-btn').click(function(){
        $('html, body').animate({scrollTop:0}, 'slow');
    });

    // Owl carousel animation
    $('.carousel').owlCarousel({
        margin: 20,
        loop:true,
        navigation:true,
        autoplay: true,
        autoplayTimeout: 3000, // Increase autoplay time
        autoplayHoverPause: true,

        responsive: {
            0:{
                items:1,
                nav:false
            },
            600:{
                items: 2,
                nav: false
            },
            1000:{
                items: 3,
                nav: false
            }
        }
    });
});
  // JavaScript for generating particles

// Define function to create particles
function createParticles() {
    const container = document.querySelector('.particle-container');
    const numParticles = 200; // Adjust as needed

    for (let i = 0; i < numParticles; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');

        // Randomize particle position and size
        const size = Math.floor(Math.random() * 20) + 10; // Random size between 10 and 30 pixels
        const x = Math.random() * container.clientWidth;
        const y = Math.random() * container.clientHeight;

        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';

        container.appendChild(particle);
    }
}

// Call the function to create particles when the page loads
window.addEventListener('DOMContentLoaded', createParticles);

