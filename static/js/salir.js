// Add this to the existing script section
$('#logoutBtn').click(function() {
    Swal.fire({
        title: '¿Cerrar sesión?',
        text: '¿Está seguro que desea salir del sistema?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#4e73df',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cerrar sesión',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '../api/auth.php?action=logout';
        }
    });
});