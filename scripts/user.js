$(function() {
    $('#confirm').hide();

    $('#delete').click(function() {
        var del = $(this);
        del.addClass('light');
        del.removeClass('delete');
        del.removeAttr('href');

        $('#confirm').show();

        return false;
    });

    $('#cancel').click(function() {
        var del = $('#delete');
        del.removeClass('light');
        del.addClass('delete');
        del.attr('href', '#');

        $('#confirm').hide();

        return false;
    });

    $('#really-delete').click(function() {
        $.post($(this).attr('href'), function() {
            document.location = '/';   
        });
        return false;
    });
});
