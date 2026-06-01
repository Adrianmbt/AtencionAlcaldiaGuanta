// Funcionalidad para protección de datos

document.addEventListener('DOMContentLoaded', function() {
    // Añadir comportamiento a los formularios
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                this.reportValidity();
            }
        });
    });
});
