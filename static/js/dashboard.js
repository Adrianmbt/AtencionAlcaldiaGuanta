$(document).ready(function() {
    // Toggle sidebar on mobile
    $('.navbar-toggler').on('click', function() {
        $('.sidebar').toggleClass('active');
    });

    // Close sidebar when clicking outside on mobile
    $(document).on('click', function(e) {
        if ($(window).width() < 768) {
            if (!$(e.target).closest('.sidebar').length && !$(e.target).closest('.navbar-toggler').length) {
                $('.sidebar').removeClass('active');
                $('#sidebarMenu').removeClass('show');
            }
        }
    });

    // Handle active menu items
    $('.nav-link').on('click', function() {
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
    });
    
    // Animación para las tarjetas de estadísticas
    $('.card-stats').each(function(index) {
        $(this).delay(100 * index).animate({opacity: 1}, 500);
    });
});
