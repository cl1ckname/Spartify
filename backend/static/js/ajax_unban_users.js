var csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
        else {console.log('blinb')}
    }
});

var loc = window.location
var wsStart = 'ws://';
if (loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + window.location.host + window.location.pathname;
var socket = new WebSocket(endpoint);

socket.onmessage = function(e){
    var data = JSON.parse(e.data)
    if (data['unbanned'])
        unban(data)
}

var unban = function(response){
    $("#unbun").trigger('reset');
    var to_unban = response['unbanned'];
    to_unban.forEach(function(item, i, arr){
        console.log($('#li-ban-'+item));
        $('#li-ban-'+item).remove();
    });
}

$(document).ready(function () {
    $('#unban').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            dataType: 'json',
            url: "/lobby/ajax/unban_users",
            success: function(){return false;},
            error: function (response) {
                alert(response['errors']);
            }
        });
        return false;
    });
})