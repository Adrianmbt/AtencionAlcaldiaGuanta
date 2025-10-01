$(document).ready(function() {
    // Toggle password visibility in modal
    $('#togglePasswordModal').click(function() {
        const passwordField = $('#clave');
        const passwordFieldType = passwordField.attr('type');
        
        if (passwordFieldType === 'password') {
            passwordField.attr('type', 'text');
            $(this).find('i').removeClass('fa-eye').addClass('fa-eye-slash');
        } else {
            passwordField.attr('type', 'password');
            $(this).find('i').removeClass('fa-eye-slash').addClass('fa-eye');
        }
    });

    // Load users table
    function loadUsuarios() {
        $.ajax({
            url: 'php/usuarios_actions.php',
            type: 'GET',
            data: { action: 'list' },
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    let html = '';
                    $.each(response.data, function(index, usuario) {
                        html += `<tr>
                            <td>${usuario.id}</td>
                            <td>${usuario.usuario}</td>
                            <td>${usuario.nombre}</td>
                            <td>${usuario.cedula}</td>
                            <td><span class="badge bg-${getRolBadgeClass(usuario.rol)}">${usuario.rol}</span></td>
                            <td>
                                <button class="btn btn-sm btn-primary edit-usuario" data-id="${usuario.id}">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-danger delete-usuario" data-id="${usuario.id}">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>`;
                    });
                    $('#tablaUsuarios tbody').html(html);
                } else {
                    alert('Error al cargar usuarios: ' + response.message);
                }
            },
            error: function() {
                alert('Error de conexión al cargar usuarios');
            }
        });
    }

    // Get badge class based on role
    function getRolBadgeClass(rol) {
        switch(rol) {
            case 'administrador': return 'danger';
            case 'operador': return 'success';
            case 'consulta': return 'info';
            default: return 'secondary';
        }
    }

    // Initial load
    if ($('#tablaUsuarios').length) {
        loadUsuarios();
    }

    // Clear form when modal is opened for new user
    $('.card-header button[data-bs-target="#modalUsuario"]').click(function() {
        $('#formUsuario')[0].reset();
        $('#idUsuario').val('');
        $('#modalUsuarioLabel').text('Nuevo Usuario');
    });

    // Edit user
    $(document).on('click', '.edit-usuario', function() {
        const id = $(this).data('id');
        
        $.ajax({
            url: 'php/usuarios_actions.php',
            type: 'GET',
            data: { action: 'get', id: id },
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    const usuario = response.data;
                    $('#idUsuario').val(usuario.id);
                    $('#usuario').val(usuario.usuario);
                    // Don't fill password field for security
                    $('#nombre').val(usuario.nombre);
                    $('#cedula').val(usuario.cedula);
                    $('#rol').val(usuario.rol);
                    
                    $('#modalUsuarioLabel').text('Editar Usuario');
                    $('#modalUsuario').modal('show');
                } else {
                    alert('Error al cargar usuario: ' + response.message);
                }
            },
            error: function() {
                alert('Error de conexión al cargar usuario');
            }
        });
    });

    // Delete user
    $(document).on('click', '.delete-usuario', function() {
        if (confirm('¿Está seguro de eliminar este usuario?')) {
            const id = $(this).data('id');
            
            $.ajax({
                url: 'php/usuarios_actions.php',
                type: 'POST',
                data: { action: 'delete', id: id },
                dataType: 'json',
                success: function(response) {
                    if (response.success) {
                        alert('Usuario eliminado correctamente');
                        loadUsuarios();
                    } else {
                        alert('Error al eliminar usuario: ' + response.message);
                    }
                },
                error: function() {
                    alert('Error de conexión al eliminar usuario');
                }
            });
        }
    });

    // Save user
    $('#btnGuardarUsuario').click(function() {
        // Basic validation
        let isValid = true;
        $('#formUsuario input, #formUsuario select').each(function() {
            if ($(this).prop('required') && $(this).val().trim() === '') {
                $(this).addClass('is-invalid');
                isValid = false;
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        if (isValid) {
            const formData = $('#formUsuario').serialize();
            const id = $('#idUsuario').val();
            const action = id ? 'update' : 'create';
            
            $.ajax({
                url: 'php/usuarios_actions.php',
                type: 'POST',
                data: formData + '&action=' + action,
                dataType: 'json',
                success: function(response) {
                    if (response.success) {
                        alert(id ? 'Usuario actualizado correctamente' : 'Usuario creado correctamente');
                        $('#modalUsuario').modal('hide');
                        loadUsuarios();
                    } else {
                        alert('Error: ' + response.message);
                    }
                },
                error: function() {
                    alert('Error de conexión al guardar usuario');
                }
            });
        }
    });
});