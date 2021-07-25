$(document).ready(function () {
    $('#remove_members').submit(function () {

        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'), 
            url: "/lobby/ajax/remove_members",
            success: function (response) {
                $("#remove_members").trigger('reset');
                var to_delete = response['to_delete'];
                console.log(typeof(to_delete));
                to_delete.forEach(function(item, i, arr){
                    $('#li-'+i).remove();
                });
                
            },
            error: function (response) {
                alert(response['errors']);
            }
        });
        return false;
    });
})