;$('head').append('<style type="text/css">.azpanes {display:none;}</style>');
$(function() {
    $("#azindexpage ul.aztabs").tabs("div.azpanes > div");
    $("#azindexpage .azpanes:hidden").show();
    $("#azindexpage div.noword a.letter-link").click(function(event) {event.preventDefault();});
});
