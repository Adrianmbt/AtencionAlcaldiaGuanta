$(document).ready(function() {
    // Funcionalidad para alternar la visibilidad de la contraseña
    $('#togglePassword').click(function() {
        const passwordInput = $('#password');
        const icon = $(this).find('i');
        
        if (passwordInput.attr('type') === 'password') {
            passwordInput.attr('type', 'text');
            icon.removeClass('fa-eye');
            icon.addClass('fa-eye-slash');
        } else {
            passwordInput.attr('type', 'password');
            icon.removeClass('fa-eye-slash');
            icon.addClass('fa-eye');
        }
    });

    // Manejar el envío del formulario de inicio de sesión
    $('#loginForm').submit(function(e) {
        e.preventDefault();
        
        const username = $('#username').val();
        const password = $('#password').val();
        
        const submitButton = $(this).find('button[type="submit"]');
        submitButton.prop('disabled', true);
        
        $.ajax({
            url: '/auth/login',
            type: 'POST',
            data: {
                usuario: username,
                clave: password
            },
            success: function(response) {
                window.location.href = '/dashboard';
            },
            error: function(xhr, status, error) {
                console.error('Error en login:', error);
                Swal.fire({
                    title: 'Error',
                    text: 'Usuario o contraseña incorrectos',
                    icon: 'error',
                    confirmButtonText: 'Aceptar'
                });
                submitButton.prop('disabled', false);
            }
        });
    });
});
