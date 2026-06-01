// Funcionalidad para cerrar sesión

function logout() {
    if (confirm('¿Está seguro de cerrar sesión?')) {
        window.location.href = '/logout';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});
