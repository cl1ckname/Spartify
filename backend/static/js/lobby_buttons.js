console.log("I am working!");


$(document).ready(function(){
    console.log("Ready");
    $("#create").click(function(){
        var choose = $("#buttons")[0];
        choose.style.display = "none"
        $("#create_lobby")[0].style.display = "block";
        });
    $("#join").click(function(){
        var choose = $("#buttons")[0];
        choose.style.display = "none"
        $("#join_lobby")[0].style.display = "block";
        });
    });