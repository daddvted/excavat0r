$(document).ready(function(){

    $("#000").click(function(){
        var msg = $("#message").val();
        ajaxRequest(msg) //ajax
    }); // menu listener
    $("#message").keyup(function(event){
        if(event.keyCode == 13) {
            var msg = $("#message").val();
            ajaxRequest(msg)
        }
    });

    function setup400CLick() {
        $("#400").click(function(){
            var code = $(this).attr("id");
            var msg = $("#message").val();
            // send2server(code, msg); //WebSocket
            ajaxRequest(code, msg); //ajax
        });
    }

    function ajaxRequest(msg) {
        var message = {
            "msg": msg
        };
        data = JSON.stringify(message);
        $.ajax({
            url: "/enquire",
            type: "POST",
            data: data,
            dataType: "json",
            beforeSend: function(){},
            success: function(data){
                parseResult(data);
            },
            error: function(){
                $("#result").html("Error happened : /")
            }
        });
    } //ajaxRequest()

    function parseResult(json) {
        alert(JSON.stringify(json));
        var code = json.code;
        var html = "";
        if(code == "000") {
            html = "<div>为您找到以下问答:<ul>";
            $.each(json.resp, function(n, item){
                html += '<li><a href="#">' + item.title+ '</a></li>';
            });
            html += "</ul></div>";

        } else if(code == "400" || code == "999") {
            html = "<p>" + json.resp + "</p>";
        }

        html += "<hr/>"
        $(html).prependTo("#result");

    } //parseResult()

});// document