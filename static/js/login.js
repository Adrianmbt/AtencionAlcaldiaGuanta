$(document).ready(function() {
    // Funcionalidad para alternar la visibilidad de la contraseña
    $('#togglePassword').click(function() {
        const passwordInput = $('#password');
        const icon = $(this).find('i');

        if (passwordInput.attr('type') === 'password') {
            passwordInput.attr('type', 'text');
            icon.removeClass('fa-eye').addClass('fa-eye-slash');
        } else {
            passwordInput.attr('type', 'password');
            icon.removeClass('fa-eye-slash').addClass('fa-eye');
        }
    });

    // Manejar el envío del formulario de inicio de sesión
    $('#loginForm').submit(function(e) {
        e.preventDefault();

        const username = $('#username').val();
        const password = $('#password').val();
        const submitButton = $(this).find('button[type="submit"]');

        submitButton.prop('disabled', true).text('Iniciando...');

        $.ajax({
            url: '/auth/login',
            type: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            data: {
                usuario: username,
                clave: password
            },
            success: function(response) {
                if (response.success) {
                    window.location.href = response.redirect || '/dashboard';
                } else {
                    Swal.fire({
                        title: 'Acceso denegado',
                        text: response.error_message || 'Usuario o contraseña incorrectos',
                        icon: 'error',
                        confirmButtonText: 'Aceptar',
                        confirmButtonColor: '#e85d45'
                    });
                    submitButton.prop('disabled', false).text('Iniciar Sesión');
                }
            },
            error: function(xhr) {
                let msg = 'Ha ocurrido un error. Intente nuevamente.';
                if (xhr.responseJSON && xhr.responseJSON.error_message) {
                    msg = xhr.responseJSON.error_message;
                } else if (xhr.status === 401) {
                    msg = 'Usuario o contraseña incorrectos';
                }
                Swal.fire({
                    title: 'Error',
                    text: msg,
                    icon: 'error',
                    confirmButtonText: 'Aceptar',
                    confirmButtonColor: '#e85d45'
                });
                submitButton.prop('disabled', false).text('Iniciar Sesión');
            }
        });
    });
});
