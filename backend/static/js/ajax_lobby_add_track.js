$(document).ready(function () {
    $('#add_track').submit(function () {

        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'), 
            url: "/lobby/ajax/add_lobby_track",
            success: function (response) {
                $("#add_track").trigger('reset');
                var Data = new Date();
                var minutes = Data.getMinutes();
                var hours = Data.getHours();
                var title = response['title'];
                var username = response['username'];
                var new_li = $('<li class="list-group-item list-group-item-action">'+title+' ' + hours + ':' + minutes +' by '+username+'</li>');
                $("#list-history").prepend(new_li)
            },
            error: function (response) {
                alert("Incorrect link!");
            }
        });
        return false;
    });
})