// Navegación y funcionalidad global

document.addEventListener('DOMContentLoaded', function() {
    // Añadir comportamiento a los enlaces de navegación
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function() {
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Añadir comportamiento al botón de logout
    const logoutBtn = document.querySelector('[href*="logout"]');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            if (!confirm('¿Está seguro de cerrar sesión?')) {
                e.preventDefault();
            }
        });
    }
});
