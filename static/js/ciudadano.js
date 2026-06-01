$(document).ready(function() {
    var tablaPersonas = $('#tablaPersonas').DataTable({
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json"
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
        ]
    });
    
    // Botón Nuevo
    $("#btnNuevo").click(function() {
        $("#formPersona").trigger("reset");
        $("#id").val("");
        $(".modal-title").text("Nueva Persona");
        $('#personaModal').modal('show');
    });
    
    // Botón Guardar
    $("#btnGuardar").click(function() {
        if (!$("#formPersona")[0].checkValidity()) {
            $("#formPersona")[0].reportValidity();
            return;
        }
        
        var formData = new FormData($("#formPersona")[0]);
        var id = $("#id").val();
        var accion = id === "" ? "crear" : "editar";
        
        formData.append("accion", accion);
        
        $.ajax({
            url: "/ciudadano",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function() {
                $('#personaModal').modal('hide');
                Swal.fire({
                    title: "¡Éxito!",
                    text: "Ciudadano guardado correctamente",
                    icon: "success",
                    confirmButtonText: "Aceptar"
                });
                tablaPersonas.ajax.reload();
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
        $('#personaModal').modal('show');
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
                    url: "/ciudadano/eliminar/" + data.id,
                    type: "GET",
                    success: function() {
                        Swal.fire({
                            title: "¡Eliminado!",
                            text: "Ciudadano eliminado correctamente",
                            icon: "success",
                            confirmButtonText: "Aceptar"
                        });
                        tablaPersonas.ajax.reload();
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
