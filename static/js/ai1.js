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

    // 901 - segment
    $("#segment_btn").click(function(){
        var msg = "901" + $("#input_txt").val();
        ws.send(msg);
    });

    // 902 - extract keyword
    $("#keyword_btn").click(function(){
        var msg = "902" + $("#input_txt").val();
        ws.send(msg);
    });

    // 903 - Word flag
    $("#flag_btn").click(function(){
        var msg = "903" + $("#input_txt").val();
        ws.send(msg);
    });



    ws.onmessage = function(event){
        $("#result").html("");
        alert(event.data)
        var content = $("<p>[Server] "+ event.data + "</p>");
        content.appendTo("#result");
    }
    ws.onerror = function(event){
        var err = $("<p>[Client] Lose connection</p>");
        err.appendTo("#result");
    }

    function setmap() {
    }

});// document