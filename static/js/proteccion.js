$(document).ready(function() {
    // Simple initialization without complex options
    if ($('#tabla_ayudas').length > 0) {
        $('#tabla_ayudas').DataTable({
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'
            },
            responsive: true,
            paging: true,
            searching: true,
            ordering: true,
            info: true,
            lengthChange: true,
            pageLength: 10,
            order: [[0, 'desc']]
        });
    }
});