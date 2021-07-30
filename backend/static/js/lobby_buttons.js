
$(document).ready(function(){
    console.log("132323");
    var baseUrl = window.location.protocol + "//" + window.location.host + window.location.pathname+window.location.search;
    var url = new URL(baseUrl);
    var p = url.searchParams.get("p");
    console.log(url)
    var choose = $("#buttons")[0];
    if (p=="create"){
        choose.style.display = "none";
        $("#create_lobby")[0].style.display = "block";
    }
    else if (p=="join"){
        choose.style.display = "none";
        $("#join_lobby")[0].style.display = "block";
    }
    $("#create").click(function(){
        choose.style.display = "none";
        $("#create_lobby")[0].style.display = "block";
        history.pushState(null, null, baseUrl + "?p=create");
        });
    $("#join").click(function(){
        var choose = $("#buttons")[0];
        choose.style.display = "none";
        $("#join_lobby")[0].style.display = "block";
        history.pushState(null, null, baseUrl + "?p=join");
        });
    });