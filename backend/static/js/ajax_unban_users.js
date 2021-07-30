var csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
        else {console.log('blinb')}
    }
});
$(document).ready(function () {
    $('#unban').submit(function () {

        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            dataType: 'json',
            url: "/lobby/ajax/unban_users",
            success: function (response) {
                $("#unbun").trigger('reset');
                var to_unban = response['unbanned'];
                to_unban.forEach(function(item, i, arr){
                    $('#li-ban-'+item).remove();
                });
                
            },
            error: function (response) {
                alert(response['errors']);
            }
        });
        return false;
    });
})