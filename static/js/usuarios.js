// Funcionalidad para gestión de usuarios

document.addEventListener('DOMContentLoaded', function() {
    // Añadir comportamiento a los botones de acción
    document.querySelectorAll('.btn-action').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
});
