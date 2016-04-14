$(document).ready(function(){
    var ws = new WebSocket("ws://localhost:8000/ws");

    //====================================
    // Handler for message and error
    //====================================
    ws.onmessage = function(event){
        var resp_json = $.parseJSON(event.data);
        parseResult(resp_json);
    }

    ws.onerror = function(event){
        var err = $("<p>Lose connection</p>");
        err.appendTo("#result");
    }

    function parseResult(json) {
        alert(JSON.stringify(json));
        var type = json.type;
        var html = "";
        if(type == "999" || type == "901" || type == "902"){
            html = "<p>" + json.resp + "</p>";
            $(html).appendTo("#result");
        } else if(type == "903") {
            html = "<div><ul>"
            $.each(json.resp, function(n, item){
                html += "<li>" + item.word+ " | " + item.flag + "</li>";
            });
            html += "</ul></div>";
            $(html).appendTo("#result");
        }

    }

    function send2server(code, msg) {
        var message = {
            'code': code,
            'msg': msg
        }
        ws.send(JSON.stringify(message))
    }

/*
    function ajaxRequestode, msg) {
        var message = {
            'code': code,
            'msg': msg
        }

        $.ajax({
            url: "/ai1",
            type: "GET",
            data: {"m":JSON.stringify(message)},
            dataType: "json",
            beforeSend: function(){},
            success: function(data){
                alert(data.hello)
            },
            error: function(){
                $("#result").html("Error happened : /")
            }
        });
    }
*/

    //====================================
    // Click handler
    //====================================


    $("#menu li a").click(function(){
        // 000 - AI
        // 901 - segment
        // 902 - extract keyword
        // 903 - Word flag
        var code = $(this).attr("id")
        var msg = $("#message").val()

        if(code == "clear"){
            $("#result").html("")
        } else {
            send2server(code, msg)
//            ajaxRequest(code, msg)
        }
    });

});// document