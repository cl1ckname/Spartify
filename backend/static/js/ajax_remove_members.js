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
    $('#remove_members').submit(function () {

        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            dataType: 'json',
            url: "/lobby/ajax/remove_members",
            success: function (response) {
                $("#remove_members").trigger('reset');
                var to_delete = response['to_delete'];
                to_delete.forEach(function(item, i, arr){
                    $('#li-'+item).remove();
                });
                
            },
            error: function (response) {
                alert(response['errors']);
            }
        });
        return false;
    });
})