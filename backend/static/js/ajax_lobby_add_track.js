var csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
        else {console.log('blinb')}
    }
});

var add_track = function (response) {
    $("#add_track").trigger('reset');
    var Data = new Date();
    var minutes = Data.getMinutes();
    var hours = Data.getHours();
    var title = response['title'];
    var username = response['username'];
    var new_li = $('<li class="list-group-item list-group-item-action">'+title+' ' + hours + ':' + minutes +' by '+username+'</li>');
    $("#list-history").prepend(new_li);
}

var loc = window.location
var wsStart = 'ws://';
if (loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + window.location.host + window.location.pathname;
var socket = new WebSocket(endpoint);

socket.onmessage = function(e){
    var data = JSON.parse(e.data)
    console.log(data)
    if (data['title']){
        add_track(data)
    }
};

$(document).ready(function () {
    $('#add_track').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'), 
            url: "/lobby/ajax/add_lobby_track",
            success: function(response){return false;},
            error: function (response) {
                alert(response['errors']);
            }
        });
        return false;
    });
})