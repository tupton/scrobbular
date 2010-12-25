$(function() {
    $('#confirm').hide();

    $('#delete').click(function() {
        $(this).addClass('light');
        $(this).removeAttr('href');
        $('#confirm').show();
    });

    $('#cancel').click(function() {
        $('#delete').removeClass('light');
        $('#delete').attr('href', '#');
        $('#confirm').hide();
    });

    $('#really-delete').click(function() {
        alert('really delete me');
    });
});
