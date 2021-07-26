$(document).ready(function () {
    $('#ban_form').submit(function () {

        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            dataType: 'json',
            url: "/lobby/ajax/ban_user",
            success: function (response) {
                $("#ban_form").trigger('reset');
                var username = response['username'];
                var li = $('<li class="list-group-item d-flex justify-content-between list-group-item-light">'+username+
                '<input class="form-check-input" type="checkbox" value="'+username+'" aria-label="..."></li>');
                $('#ban-list ul').prepend(li);
            },
            error: function (response) {
                alert(response['errors']);
            }
        });
        return false;
    });
})