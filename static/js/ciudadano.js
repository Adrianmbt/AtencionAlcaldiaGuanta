$(document).ready(function() {
    // Initialize Bootstrap 5 modal
    var personaModal = new bootstrap.Modal(document.getElementById('personaModal'));
    
    var tablaPersonas = $('#tablaPersonas').DataTable({
        "ajax": {
            "url": "../api/ciudadano.php?accion=listar",
            "dataSrc": ""
        },
        "columns": [
            {"data": "id"},
            {"data": "nombre"},
            {"data": "cedula"},
            {"data": "direccion"},
            {"data": "telefono"},
            {"data": "comuna"},
            {
                "defaultContent": "<div class='text-center'>" +
                    "<button class='btn btn-primary btn-sm btn-action btnEditar'><i class='fas fa-pencil-alt'></i></button>" +
                    "<button class='btn btn-danger btn-sm btn-action btnBorrar'><i class='fas fa-trash-alt'></i></button>" +
                    "</div>"
            }
        ],
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json"
        }
    });
    
    // Botón Nuevo
    $("#btnNuevo").click(function() {
        $("#formPersona").trigger("reset");
        $("#id").val("");
        $(".modal-title").text("Nueva Persona");
        personaModal.show();
    });
    
    // Botón Guardar
    $("#btnGuardar").click(function() {
        // Validar formulario
        if (!$("#formPersona")[0].checkValidity()) {
            $("#formPersona")[0].reportValidity();
            return;
        }
        
        var formData = new FormData($("#formPersona")[0]);
        var id = $("#id").val();
        var accion = id === "" ? "crear" : "editar";
        
        formData.append("accion", accion);
        
        $.ajax({
            url: "../api/ciudadano.php",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            dataType: "json", // Expect JSON response
            success: function(resultado) {
                if (resultado.status === "success") {
                    personaModal.hide();
                    Swal.fire({
                        title: "¡Éxito!",
                        text: resultado.message,
                        icon: "success",
                        confirmButtonText: "Aceptar"
                    });
                    tablaPersonas.ajax.reload();
                } else {
                    Swal.fire({
                        title: "Error",
                        text: resultado.message,
                        icon: "error",
                        confirmButtonText: "Aceptar"
                    });
                }
            },
            error: function(xhr, status, error) {
                console.error("Error en la solicitud:", error);
                Swal.fire({
                    title: "Error",
                    text: "Ha ocurrido un error al procesar la solicitud.",
                    icon: "error",
                    confirmButtonText: "Aceptar"
                });
            }
        });
    });
    
    // Botón Editar
    $(document).on("click", ".btnEditar", function() {
        var data = tablaPersonas.row($(this).parents("tr")).data();
        
        $("#id").val(data.id);
        $("#nombre").val(data.nombre);
        $("#cedula").val(data.cedula);
        $("#direccion").val(data.direccion);
        $("#telefono").val(data.telefono);
        $("#comuna").val(data.comuna);
        
        $(".modal-title").text("Editar Persona");
        personaModal.show();
    });
    
    // Botón Borrar
    $(document).on("click", ".btnBorrar", function() {
        var data = tablaPersonas.row($(this).parents("tr")).data();
        
        Swal.fire({
            title: "¿Está seguro?",
            text: "Esta acción no se puede deshacer",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Sí, eliminar",
            cancelButtonText: "Cancelar"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: "../api/ciudadano.php",
                    type: "POST",
                    data: {
                        id: data.id,
                        accion: "eliminar"
                    },
                    dataType: "json", // Expect JSON response
                    success: function(resultado) {
                        if (resultado.status === "success") {
                            Swal.fire({
                                title: "¡Eliminado!",
                                text: resultado.message,
                                icon: "success",
                                confirmButtonText: "Aceptar"
                            });
                            tablaPersonas.ajax.reload();
                        } else {
                            Swal.fire({
                                title: "Error",
                                text: resultado.message,
                                icon: "error",
                                confirmButtonText: "Aceptar"
                            });
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error("Error en la solicitud:", error);
                        Swal.fire({
                            title: "Error",
                            text: "Ha ocurrido un error al procesar la solicitud.",
                            icon: "error",
                            confirmButtonText: "Aceptar"
                        });
                    }
                });
            }
        });
    });
});