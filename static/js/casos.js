// Lógica adicional para el módulo de casos

// Añadir al inicio del archivo o después del DOMContentLoaded

// Función para filtrar ciudadanos en el desplegable
function configurarFiltroCiudadanos() {
    const inputBuscar = document.getElementById('buscarCiudadano');
    const selectCiudadano = document.getElementById('idP');
    
    if (inputBuscar && selectCiudadano) {
        // Guardar todas las opciones originales para poder restaurarlas
        const opcionesOriginales = Array.from(selectCiudadano.options);
        
        inputBuscar.addEventListener('input', function() {
            const textoBusqueda = this.value.toLowerCase();
            
            // Restaurar todas las opciones originales
            selectCiudadano.innerHTML = '';
            const opcionDefault = document.createElement('option');
            opcionDefault.value = '';
            opcionDefault.textContent = 'Seleccione un ciudadano';
            selectCiudadano.appendChild(opcionDefault);
            
            // Filtrar y añadir solo las que coinciden con la búsqueda
            opcionesOriginales.forEach(opcion => {
                if (opcion.value === '') return; // Saltar la opción por defecto
                
                const nombre = opcion.getAttribute('data-nombre') || '';
                const cedula = opcion.getAttribute('data-cedula') || '';
                const comuna = opcion.getAttribute('data-comuna') || '';
                const textoCompleto = `${nombre} ${cedula} ${comuna}`.toLowerCase();
                
                if (textoCompleto.includes(textoBusqueda)) {
                    selectCiudadano.appendChild(opcion.cloneNode(true));
                }
            });
            
            // Si solo hay una opción además del default, seleccionarla automáticamente
            if (selectCiudadano.options.length === 2) {
                selectCiudadano.selectedIndex = 1;
            }
        });
    }
}

// Añadir la llamada a la función dentro del DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // Validación del formulario de casos
    const formCaso = document.getElementById('formCaso');
    
    if (formCaso) {
        formCaso.addEventListener('submit', function(e) {
            if (!validarFormularioCaso()) {
                e.preventDefault();
                return false;
            }
        });
    }

    // Inicializar DataTable si está disponible
    if (typeof $ !== 'undefined' && $.fn.DataTable) {
        $('#tablaCasos').DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
            },
            responsive: true,
            pageLength: 25,
            order: [[0, 'desc']], // Ordenar por ID descendente
            columnDefs: [
                { orderable: false, targets: -1 } // Deshabilitar ordenamiento en columna de acciones
            ]
        });
    }

    // Autocompletar especificación según motivo
    const motivoCaso = document.getElementById('motivo_caso');
    const especificacionCaso = document.getElementById('especificacion_caso');
    
    if (motivoCaso && especificacionCaso) {
        motivoCaso.addEventListener('change', function() {
            const sugerencias = obtenerSugerenciasEspecificacion(this.value);
            especificacionCaso.setAttribute('list', 'sugerencias-especificacion');
            
            // Crear o actualizar datalist
            let datalist = document.getElementById('sugerencias-especificacion');
            if (!datalist) {
                datalist = document.createElement('datalist');
                datalist.id = 'sugerencias-especificacion';
                especificacionCaso.parentNode.appendChild(datalist);
            }
            
            datalist.innerHTML = '';
            sugerencias.forEach(sugerencia => {
                const option = document.createElement('option');
                option.value = sugerencia;
                datalist.appendChild(option);
            });
        });
    }

    // Formatear valor de inversión social
    const valorInversion = document.getElementById('valor_inversion_social');
    if (valorInversion) {
        valorInversion.addEventListener('input', function() {
            // Permitir solo números y punto decimal
            this.value = this.value.replace(/[^0-9.]/g, '');
            
            // Evitar múltiples puntos decimales
            const parts = this.value.split('.');
            if (parts.length > 2) {
                this.value = parts[0] + '.' + parts.slice(1).join('');
            }
        });
    }
    
    // Configurar filtro de ciudadanos
    configurarFiltroCiudadanos();
});

function validarFormularioCaso() {
    const campos = {
        idP: 'Debe seleccionar un ciudadano',
        motivo_caso: 'Debe seleccionar el motivo del caso',
        especificacion_caso: 'Debe especificar el tipo de caso',
        estado: 'Debe seleccionar el estado del caso',
        descayuda: 'Debe proporcionar una descripción del caso'
    };

    for (const [campo, mensaje] of Object.entries(campos)) {
        const elemento = document.getElementById(campo);
        if (!elemento || !elemento.value.trim()) {
            Swal.fire({
                icon: 'error',
                title: 'Campo requerido',
                text: mensaje
            });
            elemento?.focus();
            return false;
        }
    }

    // Validar valor de inversión social si se proporciona
    const valorInversion = document.getElementById('valor_inversion_social');
    if (valorInversion && valorInversion.value) {
        const valor = parseFloat(valorInversion.value);
        if (isNaN(valor) || valor < 0) {
            Swal.fire({
                icon: 'error',
                title: 'Valor inválido',
                text: 'El valor de inversión social debe ser un número válido mayor o igual a 0'
            });
            valorInversion.focus();
            return false;
        }
    }

    // Validar longitud de descripción
    const descripcion = document.getElementById('descayuda');
    if (descripcion && descripcion.value.length < 10) {
        Swal.fire({
            icon: 'error',
            title: 'Descripción insuficiente',
            text: 'La descripción debe tener al menos 10 caracteres'
        });
        descripcion.focus();
        return false;
    }

    return true;
}

function obtenerSugerenciasEspecificacion(motivo) {
    const sugerencias = {
        'Ayudas Sociales': [
            'Tanques de agua',
            'Materiales de construcción',
            'Muebles y enseres',
            'Ropa y calzado',
            'Alimentos no perecederos',
            'Kit de aseo personal',
            'Colchones y ropa de cama'
        ],
        'Ayudas Económicas': [
            'Subsidio de vivienda',
            'Apoyo para emprendimiento',
            'Auxilio funerario',
            'Apoyo educativo',
            'Subsidio de transporte',
            'Apoyo para servicios públicos'
        ],
        'Ayudas Técnicas (Médicas)': [
            'Silla de ruedas',
            'Bastón',
            'Caminador',
            'Prótesis',
            'Audífonos',
            'Lentes',
            'Equipo médico especializado'
        ],
        'Solicitud de Medicinas': [
            'Medicamentos crónicos',
            'Medicamentos especializados',
            'Suplementos nutricionales',
            'Medicamentos pediátricos',
            'Medicamentos geriátricos'
        ],
        'Quejas, Sugerencias y/o Denuncias': [
            'Queja por servicio público',
            'Denuncia por irregularidad',
            'Sugerencia de mejora',
            'Reclamo administrativo',
            'Petición ciudadana'
        ]
    };

    return sugerencias[motivo] || [];
}

// Función para exportar datos a Excel (opcional)
function exportarCasosExcel() {
    if (typeof XLSX !== 'undefined') {
        const tabla = document.getElementById('tablaCasos');
        const wb = XLSX.utils.table_to_book(tabla, {sheet: "Casos"});
        XLSX.writeFile(wb, `casos_${new Date().toISOString().split('T')[0]}.xlsx`);
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Función no disponible',
            text: 'La exportación a Excel no está disponible en este momento'
        });
    }
}

// Función para generar estadísticas rápidas
function mostrarEstadisticasCasos() {
    const filas = document.querySelectorAll('#tablaCasos tbody tr');
    const estadisticas = {
        total: filas.length,
        pendientes: 0,
        aprobados: 0,
        entregados: 0,
        remitidos: 0,
        inversionTotal: 0
    };

    filas.forEach(fila => {
        const estado = fila.cells[7].textContent.trim();
        const remitido = fila.cells[8].textContent.trim();
        const inversion = parseFloat(fila.cells[5].textContent.replace('$', '')) || 0;

        estadisticas.inversionTotal += inversion;

        switch (estado) {
            case 'Pendiente':
                estadisticas.pendientes++;
                break;
            case 'Aprobado':
                estadisticas.aprobados++;
                break;
            case 'Entregado':
                estadisticas.entregados++;
                break;
        }

        if (remitido === 'Remitido') {
            estadisticas.remitidos++;
        }
    });

    Swal.fire({
        title: 'Estadísticas de Casos',
        html: `
            <div class="text-start">
                <p><strong>Total de casos:</strong> ${estadisticas.total}</p>
                <p><strong>Pendientes:</strong> ${estadisticas.pendientes}</p>
                <p><strong>Aprobados:</strong> ${estadisticas.aprobados}</p>
                <p><strong>Entregados:</strong> ${estadisticas.entregados}</p>
                <p><strong>Remitidos:</strong> ${estadisticas.remitidos}</p>
                <p><strong>Inversión total:</strong> $${estadisticas.inversionTotal.toFixed(2)}</p>
            </div>
        `,
        icon: 'info',
        confirmButtonText: 'Cerrar'
    });
}