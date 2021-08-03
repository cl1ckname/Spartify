var csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
        else {console.log('blinb')}
    }
});

var ban = function (response) {
    $("#ban_form").trigger('reset');
    var username = response['username'];
    var userid = response['userid'];
    var li = $('<li id="li-ban-'+userid+'" class="list-group-item d-flex justify-content-between list-group-item-light">'+username+
    '<input class="form-check-input" type="checkbox" name="to_unban" value="'+userid+'" aria-label="..."></li>');
    console.log(li);
    $('#ban-list ul').prepend(li);
    return false;
};

var loc = window.location
var wsStart = 'ws://';
if (loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + window.location.host + window.location.pathname;
var socket = new WebSocket(endpoint);

socket.onmessage = function(e){
    var data = JSON.parse(e.data)
    if (data['username']){
        ban(data)
    }
}

$(document).ready(function () {
    $('#ban_form').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            dataType: 'json',
            url: "/lobby/ajax/ban_user",
            success: function(){},
            error: function (response) {
                alert(response['errors']);
            }
        });
        return false;
    });
})