export function ban(response) {
    $("#ban_form").trigger('reset');
    var username = response['username'];
    var userid = response['userid'];
    var li = $('<li id="li-ban-'+userid+'" class="list-group-item d-flex justify-content-between list-group-item-light">'+username+
    '<input class="form-check-input" type="checkbox" name="to_unban" value="'+userid+'" aria-label="..."></li>');
    console.log(li);
    $('#ban-list ul').prepend(li);
    return false;
};

export function add_user(data){
    var username = data['username'];
    var userid = data['userid'];
    var li = $('<li class="list-group-item d-flex justify-content-between list-group-item-light" id="li-'+userid+'">' + username + '</li>');
    $("#list_members").prepend(li);
}

export function add_track(data) {
    $("#add_track").trigger('reset');
    var Data = new Date();
    var minutes = Data.getMinutes();
    var hours = Data.getHours();
    var title = data['title'];
    var username = data['username'];
    var new_li = $('<li class="list-group-item list-group-item-action">'+title+' ' + hours + ':' + minutes +' by '+username+'</li>');
    $("#list-history").prepend(new_li);
}

export function remove_members(data) {
    $("#remove_members").trigger('reset');
    var to_delete = data['to_delete'];
    to_delete.forEach(function(item, i, arr){
        $('#li-'+item).remove();
    });
    return false;
}

export function unban(data){
    $("#unbun").trigger('reset');
    var to_unban = data['unbanned'];
    to_unban.forEach(function(item, i, arr){
        console.log($('#li-ban-'+item));
        $('#li-ban-'+item).remove();
    });
}
