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
    $('#add_sub').submit(function () {

        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'), 
            url: "/ajax/add_queue",
            success: function (response) {
                $("#add_sub").trigger('reset');
                var Data = new Date();
                var minutes = Data.getMinutes();
                var hours = Data.getHours();
                var title = response['title'];
                var username = response['username'];
                var new_li = $('<li class="list-group-item list-group-item-action">'+title+' ' + hours + ':' + minutes +' by '+username+'</li>');
                $("#history").prepend(new_li)
            },
            error: function (response) {
                alert("Incorrect link!");
            }
        });
        return false;
    });
})