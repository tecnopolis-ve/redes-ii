$(document).ready(function() {
    $('.dataTable').DataTable({
        responsive: true,
        stateSave: true
    });

    $('.toggle_activate_row').change(function() {
        const target = $(this).closest('tr').find('input:not(:checkbox), select, hidden');
        if($(this).is(":checked")) {
            target.prop('disabled', false);
        }else{
            target.prop('disabled', true);
        }
     });
} );