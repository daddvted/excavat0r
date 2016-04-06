$(document).ready(function(){

    var ws = new WebSocket("ws://localhost:8000/ws");

    // clear div content
    $("#clear_btn").click(function(){
       $("#result").html("");
    });

    // 000 - AI
    $("#go_btn").click(function(){
        var msg = "000" + $("#input_txt").val();
        ws.send(msg);
    });

    // 001 - segment
    $("#segment_btn").click(function(){
        var msg = "001" + $("#input_txt").val();
        ws.send(msg);
    });

    // 002 - extract keyword
    $("#keyword_btn").click(function(){
        var msg = "002" + $("#input_txt").val();
        ws.send(msg);
    });

    // 003 - Word flag
    $("#flag_btn").click(function(){
        var msg = "003" + $("#input_txt").val();
        ws.send(msg);
    });

    // 004 - extract keyword code
    $("#keyword_code_btn").click(function(){
        var msg = "004" + $("#input_txt").val();
        ws.send(msg);
    });


    // 007 - Spider
    $("spider_btn").click(function(){
        var msg = "007" + $("#input_txt").val();
        ws.send(msg)
    });
    // 009 - echo
    $("#echo_btn").click(function(){
        var msg = "009" + $("#input_txt").val();
        ws.send(msg);
    });



    ws.onmessage = function(event){
        var content = $("<p>[Server] "+ event.data + "</p>");
        content.appendTo("#result");
    }
    ws.onerror = function(event){
        var err = $("<p>[Client] Lose connection</p>");
        err.appendTo("#result");
    }

});// document