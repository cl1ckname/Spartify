
$(document).ready(function(){
    var overview_box = $("#overview");
    var settings_box = $('#settings');
    var overview_button = $('#switch button')[0];
    var settings_button = $('#switch button')[1];
    settings_button.onclick =function(){
        overview_box.addClass("moveLeft");
        settings_box.addClass("moveLeft");
        overview_button.style.background = "#ddd";
        settings_button.style.background = "#bbb";
    };
    console.log(overview_button.click);
    overview_button.onclick = function(){
        overview_box.removeClass("moveLeft")
        settings_box.removeClass("moveLeft");
        overview_button.style.background = "#bbb";
        settings_button.style.background = "#ddd";
    };
});