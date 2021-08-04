var loc = window.location
var wsStart = 'ws://';
if (loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + window.location.host + window.location.pathname;
var socket = new WebSocket(endpoint);


var add_user = function(data){
    var username = data['username'];
    var userid = data['userid'];
    var li = $('<li class="list-group-item d-flex justify-content-between list-group-item-light" id="li-'+userid+'">' + username + '</li>');
    $("#list_members").prepend(li);
}


socket.onmessage = function(e){
    var data = JSON.parse(e.data)
    if (data['event'] == "add_user"){
        add_user(data)
    }
}
