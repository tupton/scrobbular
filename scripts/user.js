$(function() {
    $('#confirm').hide();

    $('#delete').click(function() {
        $(this).addClass('light');
        $(this).removeClass('delete');
        $(this).removeAttr('href');
        $('#confirm').show();
    });

    $('#cancel').click(function() {
        $('#delete').removeClass('light');
        $('#delete').addClass('delete');
        $('#delete').attr('href', '#');
        $('#confirm').hide();
    });

    $('#really-delete').click(function() {
        $.post($(this).attr('href'), function() {
            document.location = '/';   
        });
        return false;
    });
});
