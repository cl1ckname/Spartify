import * as services from './services.js'

var functions = {"ban": services.ban,
                 "add_user": services.add_user,
                 "add_track": services.add_track,
                 "remove_members": services.remove_members,
                 "unban": services.unban}

var loc = window.location
var wsStart = 'ws://';
if (loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + window.location.host + window.location.pathname;
var socket = new WebSocket(endpoint);

socket.onmessage = function(e){
    var data = JSON.parse(e.data)
    console.log(data);
    if (data['event']){
        functions[data['event']](data);
    }
}

$(document).ready(function () {
    $('#ban_form').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            dataType: 'json',
            url: "/lobby/ajax/ban_user",
            success: function(){return false},
            error: function (response) {
                alert(response['errors']);
            }
        });
        return false;
    });
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
    $('#remove_members').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            dataType: 'json',
            url: "/lobby/ajax/remove_members",
            success: function (response) {return false;},
            error: function (response) {
                alert(response['errors']);
            }
        });
        return false;
    });
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
});