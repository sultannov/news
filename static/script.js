document.addEventListener('DOMContentLoaded', function() {
    var myCarousel = document.querySelector('#carouselExample');
    var carousel = new bootstrap.Carousel(myCarousel, {
        interval: 5000,
        wrap: true
    });
});